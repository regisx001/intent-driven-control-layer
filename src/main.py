from fastapi import FastAPI
from .api import router as api_router


app = FastAPI(title="Intent-Driven Control Layer Adapter")


app.include_router(api_router, prefix="/api", tags=["tools"])


@app.get("/")
def root():
    return {"message": app.title}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
