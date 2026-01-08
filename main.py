from fastapi import FastAPI
app = FastAPI(title="SubHub API")

@app.get("/")
async def root():
    return {"message": "Subscription Sharing API is running"}