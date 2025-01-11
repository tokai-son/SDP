import logging
import json
from enum import Enum
from dataclasses import dataclass

class MessageType(Enum):
    OFFER = "offer"
    ANSWER = "answer"
    CANDIDATE = "candidate"
    JOIN = "join"

class MessageFromType(Enum):
    HOST = "host"
    CLIENT = "client"

@dataclass
class Message:
    type: MessageType
    roomID: str
    sendFrom: MessageFromType
    description: dict

    def self_unmarshal(self) -> dict:
        return {
            "type": self.type.value,
            "roomID": self.roomID,
            "sendFrom": self.sendFrom.value,
            "description": self.description
        }

    def marshal(self) -> str:
        return json.dumps({
            "type": self.type.value,
            "roomID": self.roomID,
            "sendFrom": self.sendFrom.value,
            "description": self.description
        })

def unmarshal_message(data: str) -> Message:
    message = json.loads(data)

    # value existence check
    if "type" not in message or "roomID" not in message or "sendFrom" not in message or "description" not in message:
        raise ValueError("Invalid message")

    message = Message(
        type=MessageType(message["type"]),
        roomID=message["roomID"],
        sendFrom=MessageFromType(message["sendFrom"]),
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
    if not isinstance(message.sendFrom, MessageFromType):
        logging.error("Invalid sendFrom")
        return False
    if not isinstance(message.description, dict) or not message.description:
        logging.error("Invalid description")
        return False
    return True
