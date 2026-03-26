# app/core/exceptions.py

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError


def create_error_response(status_code: int, message: str) -> JSONResponse:
    """
    Creates a consistent error response shape for every error.
    Every error in this API will look exactly like this.
    """
    return JSONResponse(
        status_code=status_code,
        content={
            "status": "error",
            "code": status_code,
            "message": message
        }
    )


def register_exception_handlers(app: FastAPI) -> None:
    """
    Register all exception handlers with the FastAPI app.
    Call this once in main.py — it handles errors globally.
    """

    @app.exception_handler(404)
    async def not_found_handler(request: Request, exc):
        """Handles all 404 Not Found errors"""
        return create_error_response(
            status_code=404,
            message="The requested resource was not found"
        )

    @app.exception_handler(RequestValidationError)
    async def validation_error_handler(request: Request, exc: RequestValidationError):
        """
        Handles 422 Validation Errors — when user sends wrong data.
        Pydantic catches these automatically.
        We reformat them to be more readable.
        """
        # Extract the first error message from Pydantic's error list
        errors = exc.errors()
        if errors:
            first_error = errors[0]
            # Get the field name that failed validation
            field = " → ".join(str(loc) for loc in first_error["loc"])
            message = f"Validation error on field '{field}': {first_error['msg']}"
        else:
            message = "Invalid input data"

        return create_error_response(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            message=message
        )

    @app.exception_handler(IntegrityError)
    async def integrity_error_handler(request: Request, exc: IntegrityError):
        """
        Handles database integrity errors.
        e.g. trying to add duplicate item+warehouse combination
        """
        return create_error_response(
            status_code=status.HTTP_400_BAD_REQUEST,
            message="Database integrity error. This record may already exist."
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        """
        Catch-all handler for any unexpected errors.
        Prevents raw Python errors from leaking to users.
        """
        return create_error_response(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="An unexpected error occurred. Please try again."
        )