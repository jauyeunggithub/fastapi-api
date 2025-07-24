from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=30,
                          description="Username must be between 3 and 30 characters.")
    password: str = Field(..., min_length=8,
                          description="Password must be at least 8 characters long.")

    class Config:
        orm_mode = True


class UserOut(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True


class BookCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100,
                       description="Book title must be between 1 and 100 characters.")

    class Config:
        orm_mode = True


class BookOut(BaseModel):
    id: int
    title: str

    class Config:
        orm_mode = True


class EmailRequest(BaseModel):
    email: EmailStr
    message: str = Field(..., min_length=1, max_length=500,
                         description="Message should not be empty and must be less than 500 characters.")

    class Config:
        orm_mode = True
