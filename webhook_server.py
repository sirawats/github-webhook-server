import click
import uvicorn
from fastapi import FastAPI, Request
from subprocess import Popen, PIPE

app = FastAPI()
command = ["echo No command"]


@app.get("/")
async def root():
    return {"message": "I'm good"}


@app.post("/webhook")
async def webhook(request: Request):
    print("HEADERS:")
    print(request.headers)
    print("JSON:")
    print(request.json())
    return {"message": "Hello World"}


@click.command()
@click.argument("execute", ngargs=1)
@click.option("--host", default="0.0.0.0", help="Endpoint host")
@click.option("--port", default=5900, help="Endpoint port")
def main(execute: str, host: str, port: int):
    command[0] = execute
    uvicorn.run(app, host=host, port=port, log_level="info")


if __name__ == "__main__":
    main()
