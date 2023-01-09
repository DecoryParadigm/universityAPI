# AUTHENTICATION DECORATOR
from internal.task.auth_task import auth_token
from fastapi import Header


async def user_authentication(xaccess: str = Header(None)):
    try:
        user = await auth_token(xaccess)
        return dict(status=200, data=user)
    except BaseException as _:
        return dict(status=422, data="User not found!")
