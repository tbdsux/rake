import re

from fastapi import Response


def process_error(status: int):
    return Response(
        content=f"Error: {status} - fetch failed",
        status_code=500,
        media_type="text/plain",
    )


def process_custom_error(message: str, status: int = 500):
    return Response(
        content=message,
        status_code=status,
        media_type="text/plain",
    )


def remove_excessive_newlines(text: str, threshold: int = 3):
    pattern = r"\n{" + str(threshold) + r",}"
    return re.sub(pattern, "\n\n", text)
