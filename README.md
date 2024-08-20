# GitHub Webhook Server
### Overview
This Python application serves as a webhook server for GitHub. It listens for incoming webhook requests from GitHub and, upon a trigger, executes a predefined shell command. This is particularly useful for automating tasks such as pulling the latest code to your deployment server whenever new changes are pushed to a repository.

## Prerequisites
- Python 3.8 or higher
- FastAPI
- Uvicorn: an ASGI server
- A GitHub repository with webhook access

## Installation

#### Clone this repository:

```bash
git clone https://github.com/sirawats/github-webhook-server.git
```

#### Install the required packages:

```bash
pip install -r requirements.txt
```

#### Set up the environment variable for the webhook secret:

```bash
export WEBHOOK_SECRET='your_github_webhook_secret'
```
Use for verification of the webhook request. This should be set to the same value as the secret you set in your GitHub repository's webhook settings. ([docs](https://docs.github.com/en/webhooks/using-webhooks/validating-webhook-deliveries))

## Usage
To start the server, run the script with the desired command to execute upon receiving a webhook:

```bash
python3 /app/webhook_server.py --host 0.0.0.0 --port 6900 'cd /home/ubuntu/cra-2 && git pull'
```

Replace `cd /home/ubuntu/cra-2 && git pull` with the command you want to execute when the webhook is triggered.

For me, I use this command to pull the latest code from my GitHub repository to my deployment server.

## Configuration
#### The server can be configured using command-line options:

- `--host` : The host address for the server. Defaults to `0.0.0.0`.
- `--port` : The port on which the server listens. Defaults to `5900`.
- `--name` : The name of the server, used in logging. Defaults to `github_webhook_server`.

## Webhook Setup on GitHub ([docs](https://docs.github.com/en/webhooks))
1. Go to your repository on GitHub.
2. Click on **Settings** > **Webhooks** > **Add webhook**.
3. Set the Payload URL to your server's address (e.g., `http://yourserver:port/webhook`).
4. Choose `application/json` for the `Content type`.
5. Enter your **`WEBHOOK_SECRET`**.
6. Select the events for which you want to receive webhook notifications.
7. Click `Add webhook` `.




## Security
The server verifies the GitHub signature in each request to ensure it's genuinely from GitHub. Ensure your **WEBHOOK_SECRET** is secure and not publicly exposed.

## Logs
The application logs information about incoming requests and command execution results. Logs are stored in a file named **[server-name].log.**

## Contributing
Contributions to this project are welcome. Please follow standard GitHub contribution guidelines.

## License
MIT License - feel free to use and modify as needed.
