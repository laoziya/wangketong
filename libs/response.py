

def generate_response(status_code = 10000, message = 'ok', data=None):
    if data is None:
        data = []
    return {
        "status_code": status_code,
        "message":message,
        "data":data
    }
    
