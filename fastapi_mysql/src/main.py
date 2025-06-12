# main.py
import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI, APIRouter, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from starlette.middleware.cors import CORSMiddleware
from starlette_context.middleware import RawContextMiddleware

from containers import Container
from interface.user.user_router import router as user_router
from middleware import XSessionIdMiddleware, DBSessionMiddleware
from middleware.auth_middleware import AuthMiddleware

prefix = ""


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1) DI 컨테이너 리소스 초기화
    app.container.init_resources()

    # 2) 루트 로거 구성 (Mongo + 콘솔)
    app.container.log.root_logger()

    try:
        yield
    finally:
        await app.container.shutdown_resources()
        app.container.unwire()


def create_app() -> FastAPI:
    container = Container()

    app = FastAPI(
        title="API Server",
        lifespan=lifespan,
        openapi_url=f"{prefix}/openapi.json",
        docs_url=None,
        redoc_url=None,
        swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"},
    )
    app.openapi_version = "3.0.3"
    app.container = container

    # 정적 파일
    app.mount(f"{prefix}/static", StaticFiles(directory="src/static"), name="static")

    # 미들웨어
    app.add_middleware(RawContextMiddleware)
    app.add_middleware(XSessionIdMiddleware)
    app.add_middleware(DBSessionMiddleware)
    app.add_middleware(AuthMiddleware, jwt=container.utils.jwt())
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 라우터
    api_router = APIRouter(prefix=prefix)
    app.include_router(api_router)
    app.include_router(user_router, tags=["User"])

    return app


app = create_app()


@app.get("/")
async def healthcheck():
    return {"ok": True}


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(status_code=400, content=exc.errors())


# Swagger / ReDoc
@app.get(f"{prefix}/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=f"{prefix}/openapi.json",
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url=f"{prefix}/static/swagger-ui-bundle.js",
        swagger_css_url=f"{prefix}/static/swagger-ui.css",
        swagger_favicon_url=f"{prefix}/static/img/favicon.png",
    )


@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()


@app.get(f"{prefix}/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=app.title + " - ReDoc",
        redoc_js_url="/static/redoc.standalone.js",
        redoc_favicon_url=f"{prefix}/static/img/favicon.png",
        with_google_fonts=False,
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
