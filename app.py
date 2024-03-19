import logging

from src.config import Configuration

# Logging configuration
logging.basicConfig(
    filename="app.log",
    encoding="utf-8",
    level=logging.INFO,
    format="%(asctime)s %(message)s",
)


if __name__ == "__main__":
    config = Configuration()

    from src.frontend import demo

    demo.launch(server_name="0.0.0.0")
