import logging
import json
from enum import Enum
from dataclasses import dataclass

class MessageType(Enum):
    OFFER = "offer"
    ANSWER = "answer"
    CANDIDATE = "candidate"

@dataclass
class Message:
    type: MessageType
    roomID: str
    description: dict

def unmarshal_message(data: str) -> Message:
    message = json.loads(data)
    message = Message(
        type=MessageType(message["type"]),
        roomID=message["roomID"],
        description=message["description"]
    )
    if not is_valid_message(message):
        raise ValueError("Invalid message")
    return message

def is_valid_message(message: Message) -> bool:
    if not isinstance(message.type, MessageType):
        logging.error("Invalid message type")
        return False
    if not isinstance(message.roomID, str) or not message.roomID:
        logging.error("Invalid roomID")
        return False
    if not isinstance(message.description, dict) or not message.description:
        logging.error("Invalid description")
        return False
    return True
