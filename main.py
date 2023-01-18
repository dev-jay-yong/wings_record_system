from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/register")
async def sign(name: str):
    return {"message": f"Hello {name}"}
