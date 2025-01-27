from dotenv import load_dotenv
import os
env_path = os.path.join(os.path.dirname(__file__), '../.env')
load_dotenv(dotenv_path=env_path)


import logging
from logging.handlers import TimedRotatingFileHandler
import fastapi
from fastapi.responses import JSONResponse
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel
from fastapi_profiler import PyInstrumentProfilerMiddleware
from starlette.middleware import Middleware
from deepseekapi.routes import conversation


class DefaultResponse(BaseModel):
    message: str
    success: bool

def configure_logging():
    # Create a logger
    logger = logging.getLogger()
    logger.setLevel(logging.WARNING)

    # Create a file handler that rotates logs daily and keeps up to 7 backup logs
    log_handler = TimedRotatingFileHandler(
        filename='app.log',
        when='midnight',  # Rotate logs at midnight
        interval=1,  # Daily rotation
        backupCount=7,  # Keep up to 7 backup logs
        encoding='utf-8',
    )

    # Create a console handler with a higher log level to suppress console log messages
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.ERROR)

    # Create a log formatter
    log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Set the formatter for both handlers
    log_handler.setFormatter(log_formatter)
    console_handler.setFormatter(log_formatter)

    # Add the handlers to the logger
    logger.addHandler(log_handler)
    logger.addHandler(console_handler)

def add_routes(app):
    conversation.add_route(app)
    

def add_middleware(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    if os.getenv("PROFILER") == "true":
        app.add_middleware(PyInstrumentProfilerMiddleware)


def add_exception_handlers(app):
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        # Return a JSON response with details about the validation error but without the exception type
        errors = []
        for error in exc.errors():
            errors.append(error["msg"].replace("Value error,", ""))
        errors = ", ".join(errors)
        return JSONResponse(
            status_code=200,
            content=DefaultResponse(message=errors, success=False).dict(),
        )

configure_logging()
app = fastapi.FastAPI(
    title="DeepSeek API",
    description="",
    version="1.0.0"
)
add_routes(app)
add_middleware(app)
add_exception_handlers(app)
