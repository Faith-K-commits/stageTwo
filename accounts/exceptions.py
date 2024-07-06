import logging
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

logger = logging.getLogger(__name__)

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None and response.status_code == status.HTTP_400_BAD_REQUEST:
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        logger.info("Custom exception handler called. Modified status code to 422.")

    return response