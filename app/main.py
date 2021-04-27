from fastapi import FastAPI
from app.views import company

app = FastAPI()
app.include_router(company.router)

@app.get('/hello')
async def hello_world():
    return 'Hello World!'