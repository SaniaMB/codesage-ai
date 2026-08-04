from pydantic import BaseModel

class ScanRequest(BaseModel):
    repository: str