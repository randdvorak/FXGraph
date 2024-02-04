from View.base_screen import BaseScreenView

from typing import Any

from kivy.properties import ObjectProperty, StringProperty, BooleanProperty

from libs.config import *

import numpy as np

from kivymd.uix.textfield import MDTextField
from kivymd.uix.menu import MDDropdownMenu

class MainScreenView(BaseScreenView):

    button_disabled = BooleanProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.graph_added = False

    def model_is_changed(self) -> None:
        """
        Called whenever any change has occurred in the data model.
        The view in this method tracks these changes and updates the UI
        according to these changes.
        """
        if not self.graph_added:
            self.ids.graph.add_widget(self.model.current_graph)
            self.graph_added = True
        self.controller.set_basecurrency(None)
        self.controller.set_exchcurrency(None)
        self.controller.set_resolution(None)
        self.ids.basecurrency.text = ''
        self.ids.exchcurrency.text = ''
        self.ids.droptext.text = 'Resolution'
        self.button_disabled = True

    def menu_callback(self, resolution: dict[Any, Any]) -> None:
        self.ids.droptext.text = resolution.value
        self.controller.set_resolution(resolution)
        self._dropdown.dismiss()
        self.controller.set_status()

    def open_menu(self, item: Any) -> None:
        menu_items = [{'text':resolution.value, 'on_release':lambda x=resolution:self.menu_callback(x)} for resolution in self.controller.get_resolutions()]
        self._dropdown = MDDropdownMenu(caller=item, items=menu_items)
        self._dropdown.open()

class CurrencyTextField(MDTextField):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._dropdown = None
        self.controller = ObjectProperty()
        self.label = StringProperty()
    
    def keyboard_on_key_up(self, window, keycode) -> None:
        if keycode[1] == 'backspace' and len(self.text) == 0:
            self._dropdown.dismiss()
        else:
            if self._dropdown:
                self._dropdown.dismiss()
            currency_completions = self.controller.get_currencies_for_string(self.text)
            menu_items = [{'text':currency[CurrencyNameKey], 'on_release':lambda x=currency: self.menu_callback(x)} for currency in currency_completions]
            self._dropdown = MDDropdownMenu(caller=self, items=menu_items)
            self._dropdown.open()

    def menu_callback(self, currency: dict[Any, Any]) -> None:
        self.text = currency[CurrencyNameKey]
        if self.label == 'exchcurrency':
            self.controller.set_exchcurrency(currency)
        elif self.label == 'basecurrency':
            self.controller.set_basecurrency(currency)
        self._dropdown.dismiss()
        self.controller.set_status()


