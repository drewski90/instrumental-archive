from pydantic import BaseModel, Field

class UploadForm(BaseModel):
    file_category: str
    last_modified: str = Field(...)
    file_name: str = Field(..., max_length=250)
    content_type: str = Field(...)
    