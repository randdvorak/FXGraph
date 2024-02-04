import json, os, asyncio, copy

from typing import Any
from enum import StrEnum
from httpx import AsyncClient
from dotenv import load_dotenv
from datetime import date, time, datetime, timedelta
from random import randint

from .config import *

load_dotenv()

BASE_URL = "https://api.fxratesapi.com"

ENDPOINTS = {
    EndPointCurrenciesKey: f'{BASE_URL}/currencies',
    EndPointTimeSeriesKey: f'{BASE_URL}/timeseries'
}

TIMESERIES_PARAMS = {
    StartDateKey:'',
    EndDateKey:'',
    ResolutionKey:'',
    ExchangeCurrencyKey:'',
    BaseCurrencyKey:'',
    FormatKey:'json'
}

class Resolution(StrEnum):
    DAY = 'day'
    HOUR = 'hour'
    QUARTER = '15m'
    # TEN = '10m'
    # FIVE = '5m'
    # ONE = '1m'

def last_business_day(t: time):
    weekday = datetime.today().weekday()
    d = date.today()
    if weekday == 5:
        delta = timedelta(days=1)
    elif weekday == 6:
        delta = timedelta(days=2)
    bday = d - delta
    return datetime.combine(bday, t)


CUTOFF_DATES = {
    Resolution.DAY: datetime.today() - timedelta(days=364, hours=23, minutes=59, seconds=59),
    Resolution.HOUR: datetime.today() - timedelta(days=6, hours=23, minutes=59, seconds=59),
    Resolution.QUARTER: last_business_day(time(0, 0, 1)),
    # Resolution.TEN: last_business_day(time(0, 0, 1)),  ## These don't work, internal server error 
    # Resolution.FIVE: last_business_day(time(0, 0, 1)), ## at least not in the free public api
    # Resolution.ONE: last_business_day(time(0, 0, 1))
}

def date_to_str(date: datetime) -> str:
    return datetime.strftime(date, '%Y-%m-%dT%H:%M:%S.000Z')

def str_to_datetime(date: str):
    return datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.000Z')

class FXRatesAPI:

    def __init__(self) -> None:
        self._headers = {'Authorization': 'Bearer {}'.format(os.getenv(AccessTokenKey))}
        self._client = AsyncClient()
        self._runner = asyncio.Runner()
        self._currencies = None
        self._fxdata = None
                                       
    async def get_json_from_url(self, url: str, params: dict[str, str] = None) -> Any:
        response = await self._client.get(url, params=params, headers=self._headers)
        return json.loads(response.text)
    
    @property
    def currencies(self) -> list[str]:
        if not self._currencies:
            self._currencies = self._runner.run(self.get_json_from_url(ENDPOINTS[EndPointCurrenciesKey]))
        return self._currencies
    
    @property
    def fxdata(self) -> Any:
        return self._fxdata
    
    def get_timeseries_data(self, basecur: str, exchcur: str, start: datetime, end: datetime, resolution: str) -> Any:
        #TODO: Error checking end after start, start not before cutoff date, valid currencies, etc.
        req_params = copy.copy(TIMESERIES_PARAMS)
        req_params[StartDateKey] = date_to_str(start)
        req_params[EndDateKey] = date_to_str(end)
        req_params[BaseCurrencyKey] = basecur
        req_params[ExchangeCurrencyKey] = exchcur
        req_params[ResolutionKey] = resolution
        timeseries_data = self._runner.run(self.get_json_from_url(ENDPOINTS[EndPointTimeSeriesKey], params=req_params))
        return timeseries_data

    def get_fx_values(self, basecur: dict[str, Any], exchcur: dict[str, Any], resolution: Resolution):
        self._fxdata = self.get_timeseries_data(basecur[CurrencyCodeKey], exchcur[CurrencyCodeKey], CUTOFF_DATES[resolution], last_business_day(time(23, 59, 59)), resolution.value)
        x_values = list(str_to_datetime(d) for d in self._fxdata[FXRatesKey].keys())
        y_values = list(v[exchcur[CurrencyCodeKey]] for _, v in self._fxdata[FXRatesKey].items())
        return (x_values, y_values)

def main() -> None:
    fxapi = FXRatesAPI()
    basecur = fxapi.currencies[randint(0, len(fxapi.currencies) - 1)].code
    exchcur = fxapi.currencies[randint(0, len(fxapi.currencies) - 1)].code
    start = CUTOFF_DATES[Resolution.QUARTER]
    end = datetime.today() - timedelta(days=2)
    resolution = Resolution.HOUR.value
    print(fxapi.get_timeseries_data(basecur, exchcur, start, end, resolution))
    
if __name__ == '__main__':
    main()
