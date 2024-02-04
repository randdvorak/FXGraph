
from typing import Any

from kivy.properties import BooleanProperty

from libs.config import *

from View.MainScreen.main_screen import MainScreenView

class MainScreenController:
    """
    The `MainScreenController` class represents a controller implementation.
    Coordinates work of the view with the model.
    The controller implements the strategy pattern. The controller connects to
    the view to control its actions.
    """

    def __init__(self, model):
        self.model = model  # Model.main_screen.MainScreenModel
        self.view = MainScreenView(controller=self, model=self.model)

    def get_view(self) -> MainScreenView:
        return self.view
        
    def get_currencies_for_string(self, string: str) -> list[Any]:
        return [v for _, v in self.model.currencies.items() if v[CurrencyNameKey].lower().startswith(string.lower())]

    def set_status(self) -> None:
        status = self.model._exchcurrency == None or self.model._basecurrency == None or self.model._resolution == None
        self.view.button_disabled  = status

    def get_resolutions(self) -> list[Any]:
        return self.model.resolutions

    def set_resolution(self, resolution) -> None:
        self.model._resolution = resolution

    def set_exchcurrency(self, currency) -> None:
        self.model._exchcurrency = currency
    
    def set_basecurrency(self, currency) -> None:
        self.model._basecurrency = currency
