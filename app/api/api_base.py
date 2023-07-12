from fastapi import APIRouter
from abc import ABCMeta


class APIBaseClass(metaclass=ABCMeta):
    def __init__(self):
        self.router = APIRouter()  