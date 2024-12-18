# Non Interactive CF Clearance Scraper

This project uses Playwright to emulate a browser and bypass Cloudflare's non-interactive challenge to retrieve the `cf_clearance` cookie from a protected website.
![Introduction GIF](image/result.gif)

## Features

- Uses Playwright to simulate a browser.
- Bypasses Cloudflare's non-interactive challenge to retrieve the `cf_clearance` cookie.
- Supports the use of proxies and custom user agents.
- Allows configuring a timeout before giving up on retrieving the cookie.

## Running with Docker

This project is also available as a pre-built Docker image, making it quick and easy to deploy without building the image manually.  

### Requirements

- Docker installed on your machine. If you don’t have Docker installed, follow the instructions on the official [Docker website](https://www.docker.com/get-started).  

### Pull and Run the Docker Container

1. **Pull the image**:  

   You can pull the latest version of the image directly from Docker Hub:  

   ```bash
   docker pull etiennehode/non-interactive-cf-clearance-scraper:latest
   ```  

2. **Run the container**:  

   After pulling the image, run it using the following command:  

   ```bash
   docker run -d -p 5000:5000 --name cf-clearance-scraper etiennehode/non-interactive-cf-clearance-scraper:latest
   ```  

   - This starts the container in the background (`-d`) and maps port `5000` of the container to port `5000` on your local machine.  
   - Replace `5000` with any other port if `5000` is already in use.  

3. **Access the application**:  

   The server is now running and accessible at `http://localhost:5000`.  

### Environment Variables  

You can customize the behavior of the container by setting environment variables using the `-e` flag in the `docker run` command.  

| **Variable**    | **Description**                                | **Default** |
|------------------|------------------------------------------------|-------------|
| `SERVER_HOST`    | Host address where the server will bind.       | `0.0.0.0`   |
| `SERVER_PORT`    | Port the server will listen on.                | `5000`      |
| `SERVER_WORKER`  | Number of Gunicorn workers.                    | `5`         |
| `TOKEN`          | Token required for authentication (optional).  | `None`      |

Example command with environment variables:  

```bash
docker run -d -p 8080:5000 --name cf-clearance-scraper \
    -e SERVER_HOST=0.0.0.0 \
    -e SERVER_PORT=5000 \
    -e SERVER_WORKER=3 \
    -e TOKEN="your-secret-token" \
    etiennehode/non-interactive-cf-clearance-scraper:latest
```  

### Request Parameters  

The application exposes an endpoint at the root URL (`/`) to retrieve `cf_clearance` cookies using the following query parameters:  

| **Parameter**     | **Description**                                                                 | **Type**     | **Default**   |
|--------------------|---------------------------------------------------------------------------------|--------------|---------------|
| `url`             | The URL of the website requiring the `cf_clearance` cookie.                     | `string`     | `None`        |
| `user_agent`      | The User-Agent string to simulate during the request.                           | `string`     | `None`        |
| `timeout`         | Maximum duration (in seconds) to wait for the process to complete.              | `integer`    | `20`          |
| `proxy`           | Proxy server to route the request through, in the format `http://proxy:port`.   | `string`     | `None`        |
| `token`           | Optional token for authentication if `TOKEN` is defined in environment variables.| `string`     | `None`        |

#### Example Request  

```bash
curl -X GET 'http://localhost:5000/?url=https://chatgpt.com&user_agent=Mozilla/5.0&timeout=30&proxy=http://proxy:8080&token=your-secret-token'
```  

## Installation
Install Python 3.8 or higher

```bash
pip install -r requirements.txt
python -m playwright install chromium
```

## Usage

Run the script from the command line to retrieve the `cf_clearance` cookie for a given URL:

```bash
python cf_clearance_scraper.py <URL> [-ua USER_AGENT] [-t TIMEOUT] [-p PROXY] [-d]
```

### Arguments:

- `URL`: The URL where the non-interactive Cloudflare challenge is located.
- `-ua USER_AGENT`: The user agent to be used by the browser. If not specified, a random user agent will be used.
- `-t TIMEOUT`: The maximum number of seconds to wait for the cookie to be retrieved. Default is 20 seconds.
- `-p PROXY`: Proxy to be used for retrieving the cf_clearance cookie.
- `-d`: Enable debug logging for additional details during the process.

## Example

```bash
python cf_clearance_scraper.py https://chatgpt.com -ua "Mozilla/5.0" -t 30 -p "user:password@proxyserver:8080" -d
```

This command will attempt to retrieve the `cf_clearance` cookie from `https://chatgpt.com` using the provided user agent, proxy, and a 30-second timeout.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer of Liability

By using this project, you agree that you are solely responsible for how you use it. This tool is intended for educational purposes and personal use only. The author does not encourage or endorse any unauthorized or unethical use of this tool.

This project is not affiliated with Cloudflare in any way, and any use of this tool to bypass security measures may violate Cloudflare's terms of service or the terms of service of other websites. The author is not liable for any damage or consequences that may arise from using this tool. Use it at your own risk.