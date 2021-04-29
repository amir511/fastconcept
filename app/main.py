from fastapi import FastAPI
from app.views import company, user, auth

app = FastAPI()
app.include_router(company.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get('/hello')
async def hello_world():
    return 'Hello World!'