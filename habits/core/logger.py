import sys

from loguru import logger

logger.remove()  # Удаляем стандартные обработчики

# Добавляем новый обработчик для вывода в stdout в формате JSON
logger.add(
    sys.stdout,
    format="{"
    "{"
    '"time": "{time:YYYY-MM-DD HH:mm:ss}", '
    '"level": "{level}", "message": "{message}", '
    '"file": "{file}", "function": "{function}", '
    '"line": {line}'
    "}"
    "}",
)
