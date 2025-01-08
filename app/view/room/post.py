import logging
from typing import Dict

def view_request(request : Dict) -> Dict:
    name = request.get("name")
    if name is None or name == "":
        logging.error("name is required")
        raise ValueError("name is required")

    return {"name": name}

def view_response(response : Dict) -> Dict:
    roomID = response.get("roomID")
    if roomID is None or roomID == "":
        logging.error("roomID is required")
        raise ValueError("webSocketURL is required")
    return {"roomID": roomID}
