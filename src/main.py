from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.staticfiles import StaticFiles
from fastapi_swagger import patch_fastapi
from src.database import mongo_connector
from src.api.users import router as users_router
from src.api.auth import router as auth_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await mongo_connector.connect()
    yield
    mongo_connector.disconnect()

app = FastAPI(
    lifespan=lifespan,
    docs_url=None,
)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui.css",
    )

app.include_router(users_router)
app.include_router(auth_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
