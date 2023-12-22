from fastapi import FastAPI, HTTPException, Query
import logging
from loguru import logger 
import sys
from fastapi import FastAPI
from bot_trends import bot_graphic
from datetime import datetime, timedelta
from models.graph_models import Graphic
from sqlalchemy.orm import Session
from crud import multi_time_line
from database.conn import SessionLocal, engine
from models import graph_models

graph_models.Base.metadata.create_all(bind=engine)

actual_date = datetime.now()

date_one_week_ago = actual_date - timedelta(days=7)

actual_date_formated = actual_date.strftime("%d/%m/%Y")

date_formatted_one_week_ago = date_one_week_ago.strftime("%d/%m/%Y")

app = FastAPI(title='Google Trends')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

logger.add("logs/logs.log",  serialize=False)
logger.add(sys.stdout, colorize=True, format="<green>{time}</green> <level>{message}</level>", backtrace=True, diagnose=True)
logger.opt(colors=True)


@app.post('/bots')
def trends(param: str = None, country: str = None, period: str = 'Últimos 7 dias', initial_date: str = None, end_date: str = None):
    bot_graphic(param, country, period, initial_date, end_date)

@app.get("/graphics/{graphic_id}")
def read_graphic(graphic_id: int):
    db = SessionLocal()
    graphic = db.query(Graphic).filter(Graphic.id == graphic_id).first()
    db.close()
    if graphic is None:
        raise HTTPException(status_code=404, detail="Graphic not found")
    return graphic

@app.get("/graphics-all")
def read_all_graphics():
    db = SessionLocal()
    graphics = db.query(Graphic).all()
    db.close()
    return graphics


@app.get("/graphics-filters")
def read_graphics(
    date: str = Query(None, description="Filter by date"),
    param: str = Query(None, description="Filter by param"),
    value: str = Query(None, description="Filter by value")
):
    db = SessionLocal()
    
    # Construa a consulta com base nos filtros fornecidos
    query = db.query(Graphic)
    if date:
        query = query.filter(Graphic.date == date)
    if param:
        query = query.filter(Graphic.name == param)
    if value:
        query = query.filter(Graphic.value == value)
    
    graphics = query.all()
    db.close()
    return graphics

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info", reload=True)