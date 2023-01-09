from pydantic import BaseModel


class Users(BaseModel):
    iduser: int = None
    name: str = None
    location: str = None
    email: str = None

    class Config:
        orm_mode = True


class User_validation(BaseModel):
    name: str
    location: str
    email: str


class course(BaseModel):
    id: int
    title: str
    duration: str
    about: str

    class Config:
        orm_mode = True


class question_ids(BaseModel):
    quiz_id: str
    module_id: str

    class Config:
        orm_mode = True


class tracking_modules(BaseModel):
    quiz_id: str
    module_id: str
    question_id: str
    ans_value: int


class Completed_Module(BaseModel):
    quiz_id: str
    module_id: str
    score: int


class Error_Response(BaseModel):
    statusCode: int
    erorr: str


class Response_Model(BaseModel):
    statusCode: int
    data: dict
