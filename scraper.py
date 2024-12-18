from patchright.sync_api import sync_playwright, ProxySettings
from typing import Any, Optional, Dict
from fake_useragent import UserAgent
import time
import argparse
import platform

from logger import logger, logging

class CloudflareSolver:
    def __init__(
        self,
        user_agent: str,
        proxy: str
    ) -> None:
        
        if proxy:
            logger.debug(f"Proxy input -> {proxy}")
            proxy = CloudflareSolver.__parse_proxy(proxy)
            logger.debug(f"Proxy output -> {proxy}")

        logger.debug("Initializing playwright...")
        self._playwright = sync_playwright().start()
        logger.debug("Playwright initialized successfully.")

        logger.debug(f"Starting browser...")
        browser = self._playwright.chromium.launch(
            proxy=proxy, headless=False, args=["--no-sandbox", "--disable-setuid-sandbox"]
        )
        logger.debug(f"Browser started successfully!")

        context = browser.new_context(user_agent=user_agent)
        self.page = context.new_page()

    def __enter__(self):
        return self

    def __exit__(self, *_: Any) -> None:
        self._playwright.stop()

    def find_cf_clearance(self) -> Optional[str]:
        """
        This function will find cf_clearance from cookies.

        >>> find_cf_clearance()
        57oNzM4AqtD5AcO5.sZ0XnU5qg...
        """

        for cookie in self.page.context.cookies():
            if cookie["name"] == "cf_clearance":
                return cookie["value"]

    @staticmethod
    def __parse_proxy(proxy: str) -> ProxySettings:
        """
        This function is used to parse proxy.

        >>> __parse_proxy("abc:xyz@127.0.0.1:8080")
        ("127.0.0.1", 8080, "abc", "xyz")
        """

        if "@" in proxy: # Check if there is an auth
            auth, address = proxy.split("@")
            return ProxySettings(
                server=address,
                username=auth.split(":")[0],
                password=auth.split(":")[1],
            )
        
        return ProxySettings(
            server=proxy,
        )

def solve(
    url: str = None,
    user_agent: str = None,
    timeout: float = 20,
    proxy: str = None,
) -> Dict:
    """
    This function is used to retrieve the cf_clearance cookie from a non-interactive website challenge.

    >>> solve(url="https://chatgpt.com/")
    {
        "code": 200, 
        "message": "Successfully retrieved cf clearance", 
        "data":{
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0",
            "cf_clearance": "57oNzM4AqtD5AcO5.sZ0XnU5qg..."
        }
    }
    """

    try:
        if url == None:
            return {"code": 400, "message": "You must at least specify an url", "data": None}

        if user_agent is None:
            ua = UserAgent()
            user_agent = ua.random  # Generate a random user agent

        with CloudflareSolver(  # Create a Cloudflare Solver session
            user_agent=user_agent,
            proxy=proxy
        ) as solver:
            begin = time.time()  # Save begin timestamp for timeout
            logger.debug(f"Started time: {begin}")

            solver.page.goto(url)

            while (  # Wait for the CF clearance cookie to be generated, or until the timeout occurs
                time.time() - begin < timeout and
                solver.find_cf_clearance() is None
            ):
                logger.debug(f"Trying to retrieve cf clearance from cookie...")
                time.sleep(0.5)

            if cf_clearance := solver.find_cf_clearance():
                logger.debug(f"CF clearance found successfully!")
                return {"code": 200, "message": "Successfully retrieved cf clearance", "data": {"cf_clearance": cf_clearance, "user_agent": user_agent}}  # Success

            logger.debug(f"CF clearance not found")
            return {"code": 400, "message": "Unable to retrieve cf clearance (timed out)", "data": None}  # No CF Clearance in cookie
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return {"code": 500, "message": f"An error occurred, please retry. ({e})", "data": None}  # Error

def main() -> None:
    parser = argparse.ArgumentParser(
        description="This project uses Playwright to emulate a browser and bypass Cloudflare's non-interactive challenge, retrieving the cf_clearance cookie."
    )

    parser.add_argument(
        "url",
        metavar="URL",
        help="The URL where the non-interactive Cloudflare challenge is located.",
        type=str,
    )

    parser.add_argument(
        "-ua",
        "--user-agent",
        default=None,
        help="The user agent that the browser will use. If no parameter is entered, it will use a random user agent.",
        type=str,
    )

    parser.add_argument(
        "-t",
        "--timeout",
        default=20,
        help="The maximum number of seconds to retrieve the cookie.",
        type=float,
    )

    parser.add_argument(
        "-p",
        "--proxy",
        default=None,
        help="Proxy that will be used to retrieve the cf clearance cookie.",
        type=str,
    )

    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="Provides additional details on the current process.",
    )
    
    args = parser.parse_args()
    logger.setLevel(logging.DEBUG if args.debug else logging.INFO)
    
    logger.info("Trying to retrieve CF Clearance cookie...")
    result = solve(
        url=args.url,
        user_agent=args.user_agent,
        timeout=args.timeout,
        proxy=args.proxy,
    )

    logger.info(result)


if __name__ == "__main__":
    main()