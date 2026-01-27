import pytest
from app.core.logging import get_logger


class TestLogging:
    def test_get_logger(self):
        logger = get_logger("test")
        assert logger is not None
        assert logger.name == "test"

    def test_logger_levels(self):
        logger = get_logger("test.levels")
        logger.debug("Debug message")
        logger.info("Info message")
        logger.warning("Warning message")
        logger.error("Error message")
