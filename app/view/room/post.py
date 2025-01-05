from typing import Dict

def view_request(request : Dict) -> Dict:
    name = request.get("name")
    if name is None:
        raise ValueError("name is required")

    return {"name": name}

def view_response(response : Dict) -> Dict:
    websocketUrl = response.get("webSocketURL")
    if websocketUrl is None:
        raise ValueError("webSocketURL is required")
    return {"webSocketURL": websocketUrl}
