from pydantic import BaseModel

class ScrappingRequest(BaseModel):
    param: str = None
    country: str = None
    period: str = 'Últimos 7 dias'
    initial_date: str = None
    end_date: str = None
    interest_over_time: bool = True
    interest_by_subregion: bool = True
    related_issues: bool = True
    related_searches: bool = True