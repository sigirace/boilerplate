from fastapi import HTTPException, status


class UserNotFound(HTTPException):
    def __init__(self, user_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"유저 아이디 '{user_id}'를 찾을 수 없습니다.",
        )


class EmailAlreadyExists(HTTPException):
    def __init__(self, email: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"이메일'{email}'은 이미 존재합니다..",
        )


class NotAuthorized(HTTPException):
    def __init__(self, email: str):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"유저의 이메일'{email}'과 비밀번호를 확인해주세요.",
        )
