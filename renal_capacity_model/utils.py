import logging


def get_logger(module=None, level: int = logging.INFO):
    """Get logger with appropriate name."""
    logger_name = module
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s.%(funcName)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(),
        ],
    )
    return logging.getLogger(logger_name)
