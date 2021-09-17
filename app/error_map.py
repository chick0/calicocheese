from . import error
from . import error_handle


error_map = {
    # 기본 오류
    403: error_handle.e403,
    404: error_handle.e404,
    405: error_handle.e405,

    # 커스텀 오류
    error.FileIsEmpty: error_handle.file_is_empty,
    error.FileIsTooBig: error_handle.file_is_too_big,
    error.PrivateProject: error_handle.private_project,
    error.UserNotLogin: error_handle.user_not_login,
}
