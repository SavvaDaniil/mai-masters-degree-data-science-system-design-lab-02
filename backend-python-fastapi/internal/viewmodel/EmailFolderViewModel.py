from pydantic import BaseModel
from typing import Union

class EmailFolderPreviewViewModel(BaseModel):
    id: int
    title: Union[str, None]
    date_of_add: Union[str, None]