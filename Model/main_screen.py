from typing import Any

from Model.base_model import BaseScreenModel

from kivy.properties import ObjectProperty

from libs.fxratesapi import FXRatesAPI, Resolution
from libs.regressionmodel import FXRegression
from libs.grapher import Grapher
from libs.config import *

class MainScreenModel(BaseScreenModel):
    """
    Implements the logic of the
    :class:`~View.main_screen.MainScreen.MainScreenView` class.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._fxapi = FXRatesAPI()
        self._grapher = Grapher()
        self._regr = FXRegression()
        self._exchcurrency: dict[Any, Any] = None
        self._basecurrency: dict[Any, Any] = None
        self._resolution: Resolution = None
        self._current_graph = None

    @property
    def resolutions(self) -> list[Any]:
        return list(Resolution)
    
    @property
    def currencies(self) -> list[Any]:
        return self._fxapi.currencies
    
    @property
    def current_graph(self) -> Any:
        return self._current_graph
    
    def generate_graph(self) -> None:
        self._grapher.clear_graph()
        fx_x_values, fx_y_values = self._fxapi.get_fx_values(self._exchcurrency, self._basecurrency, self._resolution)
        self._grapher.add_line(fx_x_values, fx_y_values)
        regr_x_values, regr_y_values = self._regr.get_regression_data(self._fxapi.fxdata, self._basecurrency)
        self._grapher.add_line(regr_x_values, regr_y_values)
        self._grapher.set_title(f'{self._exchcurrency[CurrencyNameKey]} to {self._basecurrency[CurrencyNameKey]}')
        self._current_graph = self._grapher.graph
        self.notify_observers("main screen")

