import logging

from logging.handlers import RotatingFileHandler

logging.basicConfig(
    level=logging.DEBUG,
    filename="program.log",
    format="%(asctime)s, %(levelname)s, %(message)s, %(name)s",
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

handler = RotatingFileHandler(
    "my_logger.log", maxBytes=50000000, backupCount=5, encoding="cp1251"
)
logger.addHandler(handler)
logger.info("Какую информацию ты хотел бы получить?")
logger.warning("Большая нагрузка!")
logger.error("Бот не смог отправить сообщение")
logger.critical("Всё упало! Зовите админа!1!111")
