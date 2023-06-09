from distutils.core import USAGE
from typing import List
from typing import Any
from dataclasses import dataclass
import json

@dataclass
class Message:
    role: str
    content: str

    @staticmethod
    def from_dict(obj: Any) -> 'Message':
        _role = str(obj.get("role"))
        _content = str(obj.get("content"))
        return Message(_role, _content)

@dataclass
class Choice:
    message: Message
    finish_reason: str
    index: int

    @staticmethod
    def from_dict(obj: Any) -> 'Choice':
        _message = Message.from_dict(obj.get("message"))
        _finish_reason = str(obj.get("finish_reason"))
        _index = int(obj.get("index"))
        return Choice(_message, _finish_reason, _index)

@dataclass
class OpenAI:
    id: str
    object: str
    created: int
    model: str
    usage: USAGE
    choices: List[Choice]

    @staticmethod
    def from_dict(obj: Any) -> 'Root':
        _id = str(obj.get("id"))
        _object = str(obj.get("object"))
        _created = int(obj.get("created"))
        _model = str(obj.get("model"))
        _usage = Usage.from_dict(obj.get("usage"))
        _choices = [Choice.from_dict(y) for y in obj.get("choices")]
        return Root(_id, _object, _created, _model, _usage, _choices)

@dataclass
class Usage:
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int

    @staticmethod
    def from_dict(obj: Any) -> 'Usage':
        _prompt_tokens = int(obj.get("prompt_tokens"))
        _completion_tokens = int(obj.get("completion_tokens"))
        _total_tokens = int(obj.get("total_tokens"))
        return Usage(_prompt_tokens, _completion_tokens, _total_tokens)

# Example Usage
# jsonstring = json.loads(myjsonstring)
# root = Root.from_dict(jsonstring)
