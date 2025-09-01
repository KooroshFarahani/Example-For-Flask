from fastapi import FastAPI

app=FastAPI()
@app.get('/')
def Hello_World():
    return "Hello World"