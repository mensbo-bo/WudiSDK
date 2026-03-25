
"""
package untuk menyimpan data read only untuk websocket
yang sudah dibuat
"""
from typing import Any


class WSToken:
    def __init__(self, uuid) -> None:
        self.s_token = uuid

    def __setattr__(self, name: str, value: Any) -> Any:
        raise AttributeError("Attribute error")

    def __getstate__(self) -> object:
        return self.s_token

    def __str__(self) -> str:
        return f"{self.s_token}"
    
    def get(self):
        return self.s_token