"""
The entry point to the application.

The application uses the MVC template. Adhering to the principles of clean
architecture means ensuring that your application is easy to test, maintain,
and modernize.

You can read more about this template at the links below:

https://github.com/HeaTTheatR/LoginAppMVC
https://en.wikipedia.org/wiki/Model–view–controller
"""
import os, sys

from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivy.resources import resource_add_path
from kivy.core.window import Window

from View.screens import screens


class FXGraph(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_pallete = "BlueGray"
        Window.size = (1200, 800)
        self.load_all_kv_files(self.directory)
        # This is the screen manager that will contain all the screens of your
        # application.
        self.manager_screens = MDScreenManager()
        
    def build(self) -> MDScreenManager:
        root_dir = os.path.split(os.path.abspath(sys.argv[0]))[0]
        resource_add_path(os.path.join(root_dir, "assets", "config"))
        resource_add_path(os.path.join(root_dir, "assets", "images"))
        resource_add_path(os.path.join(root_dir, "assets", "fonts"))
        self.generate_application_screens()
        return self.manager_screens

    def generate_application_screens(self) -> None:
        """
        Creating and adding screens to the screen manager.
        You should not change this cycle unnecessarily. He is self-sufficient.

        If you need to add any screen, open the `View.screens.py` module and
        see how new screens are added according to the given application
        architecture.
        """

        for i, name_screen in enumerate(screens.keys()):
            model = screens[name_screen]["model"]()
            controller = screens[name_screen]["controller"](model)
            view = controller.get_view()
            view.manager_screens = self.manager_screens
            view.name = name_screen
            self.manager_screens.add_widget(view)


FXGraph().run()
