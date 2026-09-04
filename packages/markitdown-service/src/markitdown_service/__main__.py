# SPDX-License-Identifier: MIT
import os

import uvicorn


def main():
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run("markitdown_service.app:app", host=host, port=port)


if __name__ == "__main__":
    main()
