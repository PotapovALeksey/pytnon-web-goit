def query_exception_handler(query):
    def wrapper(*args, **kwargs):
        try:
            return query(*args, **kwargs)
        except Exception as error:
            return error

    return wrapper
