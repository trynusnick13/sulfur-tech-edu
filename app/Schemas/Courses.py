from pydantic import BaseModel
from typing import Optional, Dict


class CourseCreate(BaseModel):
    course_name: str
    course_price: float
    course_description: Optional[str]
    image: Optional[Dict[str, str]]


class CourseUpdate(BaseModel):
    course_name: Optional[str]
    course_price: Optional[float]
    course_description: Optional[str]
    image: Optional[Dict[str, str]]


class CourseSubscribe(BaseModel):
    course_id: int


class FailResponse(BaseModel):
    success: bool
    message: str


class CourseRate(BaseModel):
    rate: int
