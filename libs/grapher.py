from typing import Any

import matplotlib
matplotlib.use('module://kivy.garden.matplotlib.backend_kivyagg')
import matplotlib.pyplot as plt

from datetime import datetime

from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg

class FXGraphCanvas(FigureCanvasKivyAgg):
    """ I had to subclass and override these methods due to 
        missing implementation in superclass.
        I suppose they're meant so that you can make your 
        graphs interactive
    """
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def motion_notify_event(*args, **kwargs) -> None:
        pass

    def button_press_event(*args, **kwargs) -> None:
        pass

    def button_release_event(*args, **kwargs) -> None:
        pass

class Grapher:
    
    def __init__(self):
        self._current_figure, self._ax  = plt.subplots()
        self._canvas = FXGraphCanvas(figure=self._current_figure)

    def clear_graph(self) -> None:
        plt.cla()

    def set_title(self, title: str) -> None:
        plt.title(title)
        self._canvas.draw()

    def add_line(self, x_values: list[datetime], y_values: list[float]):
        self._ax.xaxis_date()
        plt.plot(x_values, y_values)
        self._canvas.draw()

    @property
    def graph(self) -> Any:
        return self._canvas


