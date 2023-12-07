from fastapi import FastAPI
import logging
from loguru import logger 
import sys
from fastapi import FastAPI
from bot_trends import bot_graphic
from datetime import datetime, timedelta

actual_date = datetime.now()

date_one_week_ago = actual_date - timedelta(days=7)

actual_date_formated = actual_date.strftime("%d/%m/%Y")

date_formatted_one_week_ago = date_one_week_ago.strftime("%d/%m/%Y")

app = FastAPI(title='Google Trends')

logger.add("logs/logs.log",  serialize=False)
logger.add(sys.stdout, colorize=True, format="<green>{time}</green> <level>{message}</level>", backtrace=True, diagnose=True)
logger.opt(colors=True)

@app.post('/bots')
def trends(param: str = None, country: str = None, period: str = 'Últimos 7 dias', initial_date: str = None, end_date: str = None):
    bot_graphic(param, country, period, initial_date, end_date)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info", reload=True)