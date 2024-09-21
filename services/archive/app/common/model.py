from pydantic import BaseModel


class ConnectionInfo(BaseModel):
    dbname: str
    user: str
    host: str
    password: str
    port: int = 5432
