import logging


def get_logger(name: str, env: str) -> logging.Logger:
    logger = logging.getLogger(name)

    if env == "PROD":
        logging_level = logging.INFO
    else:
        logging_level = logging.DEBUG

    logger.setLevel(level=logging_level)
    
    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging_level)

    # create formatter
    formatter = logging.Formatter(
            "%(levelname)s:\t%(message)s"
    )

    # add formatter to ch
    ch.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(ch)
    return logger
