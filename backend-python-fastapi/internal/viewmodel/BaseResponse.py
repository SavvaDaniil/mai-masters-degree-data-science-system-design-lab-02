from pydantic import BaseModel
from typing import Union, List

from internal.viewmodel.UserViewModel import UserProfileViewModel, UserSearchMicroViewModel
from internal.viewmodel.EmailFolderViewModel import EmailFolderPreviewViewModel
from internal.viewmodel.EmailViewModel import EmailLiteViewModel

class BaseResponse(BaseModel):
    status: Union[str, None] = None
    error: Union[str, None] = None
    is_auth: bool = False
    access_token: Union[str, None] = None
    forget_id: int = 0

    userProfileViewModel: Union[UserProfileViewModel, None] = None
    userSearchMicroViewModels: Union[List[UserSearchMicroViewModel], None] = None
    emailFolderPreviewViewModels: Union[List[EmailFolderPreviewViewModel], None] = None
    emailLiteViewModel: Union[EmailLiteViewModel, None] = None
    emailLiteViewModels: Union[List[EmailLiteViewModel], None] = None