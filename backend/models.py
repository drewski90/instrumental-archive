from pydantic import BaseModel, Field

class InstrumentalUploadForm(BaseModel):
    last_modified: str = Field(...)
    file_name: str = Field(..., max_length=250)
    content_type: str = Field(...)