from fastapi import APIRouter, Depends, Query
from dependency_injector.wiring import Provide, inject

from application.user.create_user import CreateUser
from containers import Container
from interface.user.user_dto import (
    CreateUserRequest,
    LoginRequest,
    LoginResponse,
    UserListResponse,
    UserResponse,
)
from interface.user.user_mapper import UserInterfaceMapper
from sqlalchemy.ext.asyncio import AsyncSession

from interface.dependency.db_session import get_session
from application.user.get_list_users import GetListUsers
from application.user.delete_user import DeleteUser
from common.dto import DeleteResponse
from application.user.login import Login
from interface.dependency.auth import get_current_user

router = APIRouter(prefix="/user")


@router.post("/signup", response_model=UserResponse)
@inject
async def signup(
    request: CreateUserRequest,
    create_user: CreateUser = Depends(Provide[Container.user_app.create_user]),
    session: AsyncSession = Depends(get_session),
):

    user = await create_user(
        name=request.name,
        email=request.email,
        password=request.password,
        session=session,
    )

    return UserInterfaceMapper.to_response(
        user=user,
    )


@router.get("/list", response_model=UserListResponse)
@inject
async def user_list(
    page: int = Query(default=1, description="조회할 페이지"),
    item_per_page: int = Query(default=10, description="페이지 당 조회할 개수"),
    user_list: GetListUsers = Depends(Provide[Container.user_app.get_list_users]),
    user_id: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):

    user_list = await user_list(
        page=page,
        item_per_page=item_per_page,
        session=session,
    )

    return UserInterfaceMapper.to_list_response(
        user_list=user_list,
    )


@router.delete("/{user_id}")
@inject
async def delete_user(
    user_id: str,
    delete_user: DeleteUser = Depends(Provide[Container.user_app.delete_user]),
    session: AsyncSession = Depends(get_session),
    current_user: dict = Depends(get_current_user),
):

    await delete_user(
        user_id=user_id,
        session=session,
    )

    return DeleteResponse(
        detail=f"{user_id}가 삭제 되었습니다.",
    )


@router.post("/login", response_model=LoginResponse)
@inject
async def delete_user(
    request: LoginRequest,
    login: Login = Depends(Provide[Container.user_app.login]),
    session: AsyncSession = Depends(get_session),
):

    access_token, refresh_token = await login(
        email=request.email,
        password=request.password,
        session=session,
    )

    return LoginResponse(
        access_token=access_token,
        refresh_token=refresh_token,
    )
