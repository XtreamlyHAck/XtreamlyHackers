from fastapi import FastAPI
from server.controllers import routers
from server.repositories.data_observer import DataObserver

app = FastAPI()

for router in routers:
    app.include_router(router)


@app.on_event("startup")
async def on_startup():
    DataObserver().start()


@app.on_event("shutdown")
async def on_shutdown():
    DataObserver().stop()


@app.get("/")
async def health():
    return {"status": "ok"}
