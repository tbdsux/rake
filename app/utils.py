import re

from fastapi import Response


def process_error(status: int):
    Response(
        content=f"Error: {status} - fetch failed",
        status_code=500,
        media_type="text/plain",
    )


def remove_excessive_newlines(text: str, threshold: int = 3):
    pattern = r"\n{" + str(threshold) + r",}"
    return re.sub(pattern, "\n\n", text)
