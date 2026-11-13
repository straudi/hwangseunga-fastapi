from pydantic import BaseModel,ConfigDict
from datetime import datetime

class File(BaseModel):
    #id : int
    filename : str
    #username : str
    uploaded_at : datetime
    #file_size : int 
    file_type : str
    file_path : str

    model_config = ConfigDict(from_attributes=True)
