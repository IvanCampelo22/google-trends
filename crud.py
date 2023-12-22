from sqlalchemy.orm import Session
from models.graph_models import Graphic

def multi_time_line(db: Session):
    result = db.query(Graphic)
    return result