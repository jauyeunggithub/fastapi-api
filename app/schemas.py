from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    username: str
    password: str


class UserOut(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True


class BookCreate(BaseModel):
    title: str


class BookOut(BaseModel):
    id: int
    title: str

    class Config:
        orm_mode = True


class EmailRequest(BaseModel):
    email: EmailStr
    message: str
