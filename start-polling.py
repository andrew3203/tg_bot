import logging
from app.bot import app

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)


if __name__ == "__main__":
    app.application = app.setup_application(is_webhook=False)
    app.run_polling(app.application)
