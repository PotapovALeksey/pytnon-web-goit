def get_response_data(data, total=None):
    response = {
        "data": data,
    }

    if total is not None:
        response["meta"] = {"total": total}

    return response
