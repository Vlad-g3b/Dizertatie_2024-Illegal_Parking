import array
from re import L
from sqlite3 import Date
from turtle import st
from numpy import number
from pydantic import BaseModel

class TrafficViolation(BaseModel):
    tf_id: str
    tf_type: str
    description: str | None = None
    location: list | None = None
    is_resolved: float | None = None

class User(BaseModel):
    usr_id: int | None = None
    usr_name: str | None = None
    usr_email: str
    usr_role: str | None = None
    usr_creation_date: Date | None = None

class ParkingSite(BaseModel):
    ps_id: str
    ps_description: str | None = None
    ps_location: str | None = None
    ps_max_parking_spots: int | None = None


class ParkingSiteList(BaseModel):
    parking_list : list | None = None