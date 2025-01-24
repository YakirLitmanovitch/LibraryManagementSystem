import logging

def log_execution(func):
    """
    Decorator to log the execution of a function
    :param func:
    :return:
    """
    def wrapper(*args, **kwargs):
        logging.info(f"Executing {func.__name__} with args: {args} and kwargs: {kwargs}")
        result = func(*args, **kwargs)
        logging.info(f"{func.__name__} returned {result}")
        return result
    return wrapper