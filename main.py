from fastapi import FastAPI
import argparse
import uvicorn

app = FastAPI()
@app.get('/')

def hello_word():
    return {"message": "Hello World"}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run FastAPI with optional file watching.")
    parser.add_argument("--watch", action="store_true", help="Enable auto-reload for the server.")
    args = parser.parse_args()


    uvicorn.run(
            app,
            host="127.0.0.1",
            port=8000,
            reload=args.watch  # Enable reload if --watch flag is passed
        )