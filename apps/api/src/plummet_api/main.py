"""Start the API: `plummet-api`."""

import uvicorn

from plummet_api.app import create_app
from plummet_core.config import get_settings


def main() -> None:
    settings = get_settings()
    uvicorn.run(create_app(settings=settings), host=settings.api_host, port=settings.api_port)


if __name__ == "__main__":
    main()
