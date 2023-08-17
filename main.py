from fastapi import FastAPI

app = FastAPI()


@app.post("/pessoas")
async def create_person():
    return {"message": "This action create a person"}


@app.get("/pessoas")
async def get_persons(t: str = None):
    return {"message": f"This action return all peoples"}


@app.get("/contagem-pessoas")
async def get_count():
    return {"message": "This action return count of peoples"}

