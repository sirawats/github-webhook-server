import click
import uvicorn
from fastapi import FastAPI, Request
from subprocess import Popen, PIPE

app = FastAPI()
command = ["echo 'nothing to execute.'"]


@app.get("/")
async def root():
    return {"message": "I'm good"}


@app.post("/webhook")
async def webhook(request: Request):
    print("HEADERS:")
    print(request.headers)
    print("JSON:")
    print(f"{request.json()}")
    return {"message": "Hello World"}


@click.command()
@click.option("--host", default="0.0.0.0", help="Endpoint host")
@click.option("--port", default=5900, help="Endpoint port")
@click.argument("execute")
def main(host: str, port: int, execute: str):
    command[0] = execute
    uvicorn.run(app, host=host, port=port, log_level="info")


if __name__ == "__main__":
    main()
