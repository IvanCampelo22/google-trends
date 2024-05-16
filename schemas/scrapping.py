from pydantic import BaseModel

class ScrappingRequest(BaseModel):
    param: str = None
    country: str = None
    period: str = 'Últimos 7 dias'
    initial_date: str = None
    end_date: str = None