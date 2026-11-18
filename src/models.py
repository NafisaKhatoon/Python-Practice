from typing import Any

from pydantic import BaseModel


class ParamDef(BaseModel):
    type: str  # "number", "integer", "string" or "boolean"


class FunctionDef(BaseModel):
    name: str
    description: str
    parameters: dict[str, ParamDef]


class PromptItem(BaseModel):
    prompt: str


class FunctionCall(BaseModel):
    prompt: str
    name: str
    parameters: dict[str, Any]
