import click
import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.templating import Jinja2Templates
from subprocess import Popen, PIPE
import hashlib
import hmac
import os
import logging
from datetime import datetime


# Config Logging
logger = logging.Logger("default_webhook_server_log")


def verify_signature(payload_body, secret_token, signature_header):
    """
    Verify that the payload was sent from GitHub by validating SHA256.

    Raise and return 403 if not authorized.

    Args:
        payload_body: original request body to verify (request.body())
        secret_token: GitHub app webhook token (WEBHOOK_SECRET)
        signature_header: header received from GitHub (x-hub-signature-256)
    """
    if not signature_header:
        raise HTTPException(status_code=403, detail="x-hub-signature-256 header is missing!")
    hash_object = hmac.new(secret_token.encode("utf-8"), msg=payload_body, digestmod=hashlib.sha256)
    expected_signature = "sha256=" + hash_object.hexdigest()
    if not hmac.compare_digest(expected_signature, signature_header):
        raise HTTPException(status_code=403, detail="Request signatures didn't match!")


app = FastAPI()
templates = Jinja2Templates(directory="templates")
command = ["echo 'nothing to execute.'"]
state = {
    "webhook_datetime": "N/A",
    "webhook_status": "N/A",
    "execute_datetime": "N/A",
    "execute_status": "N/A",
}


@app.get("/")
async def root():
    """
    Returns a JSON response with the message "Ok."
    """
    return {"message": "Ok."}


@app.post("/webhook")
async def webhook(request: Request):
    """
    Handle incoming webhook requests. Validate signature and execute command.

    Args:
        request (Request): The incoming request object.

    Returns:
        dict: The response containing the status of the webhook processing.

    Raises:
        HTTPException: If the request signature is invalid.
    """
    logger.info(request.headers)
    json_ = await request.json()
    logger.info(json_)
    try:
        state["webhook_status"] = "Processing..."
        state["webhook_datetime"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        verify_signature(await request.body(), os.environ["WEBHOOK_SECRET"], request.headers["x-hub-signature-256"])
    except HTTPException as e:
        state["webhook_status"] = "Failed"
        return e.detail
    state["webhook_status"] = "Success"

    # Execute command
    state["execute_datetime"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    state["execute_status"] = "Processing..."
    process = Popen(command[0], shell=True, stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    state["execute_datetime"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Log the command execution
    if process.returncode != 0:
        state["execute_status"] = "Failed"
        return {"status": "failed", "stdout": stdout, "stderr": stderr}
    else:
        state["execute_status"] = "Success"

    logger.info(f"Executing command: {command[0]}")
    logger.info(f"stdout: {stdout}")
    logger.info(f"stderr: {stderr}")
    return {"status": "success"}


@app.get("/monitor")
async def monitor(request: Request):
    context = {"request": request}
    for key, value in state.items():
        context[key] = value

    return templates.TemplateResponse("index.html", context)


@click.command()
@click.option("--host", default="0.0.0.0", help="Endpoint host")
@click.option("--port", default=5900, help="Endpoint port")
@click.option("--name", default="github_webhook_server", help="Name of the server")
@click.argument("execute")
def main(host: str, port: int, name: str, execute: str):
    """
    Main function to start the GitHub webhook server.

    Args:
        host (str): The host address for the server. Default is "0.0.0.0".
        port (int): The port number for the server. Default is 5900.
        name (str): The name of the server. Default is "github_webhook_server".
        execute (str): The command to execute when a webhook event is received.

    Returns:
        None
    """
    command[0] = execute

    # Config logging
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    file_handler = logging.FileHandler(f"{name}.log", mode="a+")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.addHandler(handler)

    uvicorn.run(app, host=host, port=port, log_level="info")


if __name__ == "__main__":
    main()
