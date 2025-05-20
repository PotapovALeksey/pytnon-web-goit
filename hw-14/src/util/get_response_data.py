def get_response_data(data, *, detail=None, total=None):
    response = {
        "data": data,
        "detail": detail,
    }

    if total is not None:
        response["meta"] = {"total": total}

    return response
