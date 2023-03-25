import logging


def database_logger(function):
    def wrapper(*args, **kwargs):
        logging.info(f"Database: {function.__name__} in {str(args[0].table).lower()}.")
        return function(*args, **kwargs)
    return wrapper
