from fastapi import FastAPI


app = FastAPI(title="Hello This is Indent adapter")


@app.get("/")
def root():
    return {"message": app.title}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
