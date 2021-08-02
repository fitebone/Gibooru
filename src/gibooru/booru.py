import httpx
import asyncio
from abc import ABC

class Gibooru(ABC):
    def __init__(self):
        self.client = httpx.AsyncClient()
