def query_logger(query_number: int):
    def decorator(query):
        def wrapper(*args, **kwargs):
            result = query(*args, **kwargs)
            print(f"===============Query {query_number} START===============")
            print(result)
            print(f"===============Query {query_number} END===============")

        return wrapper

    return decorator
