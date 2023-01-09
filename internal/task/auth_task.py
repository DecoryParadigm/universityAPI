'''
author: Decory Herbert
Date: 2022/11/30
description: Small tasks are hosted here. 
'''
from fastapi import status, HTTPException, Request, Header
from .. import crud
from jose import JWTError, jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv

import os

# settings
load_dotenv(".env")
ALGORITHM = "HS256"
SECRET_KEY = os.getenv("SECRET_KEY")


async def login_validation(params):
    db = await crud.validate_email(params.email)
    if len(db) > 0:
        token = await generate_token(data=dict(db[0]))
        return token
    else:
        ''' 
        If the user is not found we need to decide 
        what we are going to do for this section.
        '''
        return "User not found"


# Generate token
async def generate_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=1440)
    to_encode["exp"] = expire
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# decode token
async def auth_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
