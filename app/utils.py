
def build_response(
        status: str,
        message: str,
        data: str
):
    return {
        "status": status,
        "message": message,
        "data" : data
    }