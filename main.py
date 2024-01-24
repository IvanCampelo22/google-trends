from fastapi import FastAPI, HTTPException, Query
import logging
from loguru import logger 
import sys
from fastapi import FastAPI
from bot.scrapping import Scrapping
from datetime import datetime, timedelta
from models.graph_models import Graphic
from models.geo_map_models import GeoMap
from models.related_entities_models import RelatedEntitiesTop, RelatedEntitiesRising
from models.related_queries_models import RelatedQueriesTop, RelatedQueriesRising
from sqlalchemy.orm import Session
from database.conn import SessionLocal, engine
from models import graph_models

graph_models.Base.metadata.create_all(bind=engine)

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


@app.post('/scrapping')
def trends(param: str = None, country: str = None, period: str = 'Últimos 7 dias', initial_date: str = None, end_date: str = None):
    Scrapping.gooole_trends(param, country, period, initial_date, end_date)


@app.get("/multi-timeline")
def multi_timeline_filters(
    date: str = Query(None, description="Filter by date"),
    param: str = Query(None, description="Filter by param"),
    value: str = Query(None, description="Filter by value")
):
    db = SessionLocal()
    
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


@app.get("/geo-map")
def get_all_geo_map_data(
    param: str = Query(None, description="Filter by param"),
    region: str = Query(None, descrption="Filter by region"),
    initial_date: str = Query(None, description="Filter by initial date"),
    end_date: str = Query(None, description="Filter by end date")
):
    db = SessionLocal()

    query = db.query(GeoMap)
    if param: 
        query = query.filter(GeoMap.param == param)
    if region:
        query = query.filter(GeoMap.region == region)
    if initial_date:
        query = query.filter(GeoMap.initial_date == initial_date)
    if end_date:
        query = query.filter(GeoMap.end_date == end_date)

    geomap = query.all()
    db.close()
    return geomap


@app.get("/related-entities-top")
def related_entities_top(
    param: str = Query(None, description="Flter by param"),
    region: str = Query(None, description="Filter by region"),
    initial_date: str = Query(None, description="Filter by initial date"),
    end_date: str = Query(None, description="Filter by end_date")

):
    db = SessionLocal()

    query = db.query(RelatedEntitiesTop)
    if param:
        query = query.filter(RelatedEntitiesTop.param == param)
    if region:
        query = query.filter(RelatedEntitiesTop.region == region)
    if initial_date:
        query = query.filter(RelatedEntitiesTop.initial_date == initial_date)
    if end_date:
        query = query.filter(RelatedEntitiesTop.end_date == end_date)

    related_entities_top = query.all()
    db.close()
    return related_entities_top


@app.get("/related-entities-rising")
def related_entities_rising(
    param: str = Query(None, description="Flter by param"),
    region: str = Query(None, description="Filter by region"),
    initial_date: str = Query(None, description="Filter by initial date"),
    end_date: str = Query(None, description="Filter by end_date")

):
    db = SessionLocal()

    query = db.query(RelatedEntitiesRising)
    if param:
        query = query.filter(RelatedEntitiesRising.param == param)
    if region:
        query = query.filter(RelatedEntitiesRising.region == region)
    if initial_date:
        query = query.filter(RelatedEntitiesRising.initial_date == initial_date)
    if end_date:
        query = query.filter(RelatedEntitiesRising.end_date == end_date)

    related_entities_rising = query.all()
    db.close()
    return related_entities_rising


@app.get("/related-queries-top")
def related_queries_top(
    param: str = Query(None, description="Flter by param"),
    region: str = Query(None, description="Filter by region"),
    initial_date: str = Query(None, description="Filter by initial date"),
    end_date: str = Query(None, description="Filter by end_date")

):
    db = SessionLocal()

    query = db.query(RelatedQueriesTop)
    if param:
        query = query.filter(RelatedQueriesTop.param == param)
    if region:
        query = query.filter(RelatedQueriesTop.region == region)
    if initial_date:
        query = query.filter(RelatedQueriesTop.initial_date == initial_date)
    if end_date:
        query = query.filter(RelatedQueriesTop.end_date == end_date)

    related_queries_top = query.all()
    db.close()
    return related_queries_top


@app.get("/related-queries-rising")
def related_queries_top(
    param: str = Query(None, description="Flter by param"),
    region: str = Query(None, description="Filter by region"),
    initial_date: str = Query(None, description="Filter by initial date"),
    end_date: str = Query(None, description="Filter by end_date")

):
    db = SessionLocal()

    query = db.query(RelatedQueriesRising)
    if param:
        query = query.filter(RelatedQueriesRising.param == param)
    if region:
        query = query.filter(RelatedQueriesRising.region == region)
    if initial_date:
        query = query.filter(RelatedQueriesRising.initial_date == initial_date)
    if end_date:
        query = query.filter(RelatedQueriesRising.end_date == end_date)

    related_queries_rising = query.all()
    db.close()
    return related_queries_rising


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=5000, log_level="info", reload=True)