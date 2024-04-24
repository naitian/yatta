import uvicorn

def cli():
    print("Hello from yatta.cli")
    uvicorn.run("yatta.server.app:app", port=8000, reload=True)