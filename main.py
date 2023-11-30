from fastapi import FastAPI
import logging
from loguru import logger 
import sys
from fastapi import FastAPI
from bot_trends import bot_graphic


app = FastAPI(title='Google Trends')

logger.add("logs/logs.log",  serialize=False)
logger.add(sys.stdout, colorize=True, format="<green>{time}</green> <level>{message}</level>", backtrace=True, diagnose=True)
logger.opt(colors=True)

@app.post('/bots')
def trends(param: str = None, country: str = None):
    bot_graphic(param, country)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info", reload=True)