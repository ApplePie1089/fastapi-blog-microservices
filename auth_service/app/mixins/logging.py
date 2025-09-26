import logging


class LoggingMixin:
    def __init__(self):
        super().__init__()
        self._setup_logging()

    def _setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(levelname)s  [%(name)s] %(message)s',
            force=True
        )
        self.logger = logging.getLogger(self.__class__.__name__)