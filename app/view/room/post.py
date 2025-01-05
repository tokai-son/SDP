from typing import Dict

def view_request(request : Dict) -> Dict:
    name = request.get("name")
    if name is None:
        raise ValueError("name is required")

    return {"name": name}

def view_response(response : Dict) -> Dict:
    roomID = response.get("roomID")
    if roomID is None:
        raise ValueError("webSocketURL is required")
    return {"roomID": roomID}
