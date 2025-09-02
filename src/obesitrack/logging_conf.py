import json
import logging


class JsonFormatter(logging.Formatter):
	def format(self, record: logging.LogRecord) -> str:
		base = {
			"level": record.levelname,
			"message": record.getMessage(),
			"logger": record.name,
		}
		if record.exc_info:
			base["exception"] = self.formatException(record.exc_info)
		return json.dumps(base)


def setup_logging():
	handler = logging.StreamHandler()
	handler.setFormatter(JsonFormatter())
	root = logging.getLogger()
	root.setLevel(logging.INFO)
	root.handlers = [handler]