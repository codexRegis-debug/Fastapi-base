from pydantic import BaseModel
from typing import Any, Dict, List

class CheckPointRegister(BaseModel):
    name: str
    remote_url: str
    task_type: str = 'classification'
    input_schema: Dict[str, Any] = {}
    output_schema: Dict[str, Any] = {}

class PredictRequest(BaseModel):
    inputs: List[List[float]]
