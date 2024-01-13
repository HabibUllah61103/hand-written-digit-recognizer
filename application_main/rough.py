# from kivy.lang import Builder
# from kivy.metrics import dp
# from kivy.properties import ObjectProperty
# from kivy.uix.screenmanager import Screen
# from kivymd.app import MDApp
# from kivymd.uix.card import MDCard
# from kivymd.uix.label import MDLabel
# from CS_21076_2 import DataHandler
#
# class ElementCard(MDCard, DataHandler):
#     def __init__(self, num, **kwargs):
#         super().__init__(**kwargs)
#         self.name =
# class MyScreen(Screen):
#     grids = ObjectProperty(None)
#
#     def on_grids(self, *args):
#
#         for i in range(12):
#             self.grids.add_widget(ElementCard(i))
#
#
# class MyApp(MDApp):
#     def build(self):
#         kv = Builder.load_file("rough.kv")
#         return kv
#
# MyApp().run()
#

# from kivymd.app import MDApp
# from kivy.clock import Clock
# from kivy.lang import Builder
# from kivy.factory import Factory
# from kivy.properties import StringProperty
#
# from kivymd.uix.button import MDIconButton
# from kivymd.icon_definitions import md_icons
# from kivymd.uix.list import ILeftBodyTouch, OneLineIconListItem
# from kivymd.theming import ThemeManager
# from kivymd.utils import asynckivy
#
# Builder.load_string('''
# <ItemForList>
#     text: root.text
#
#     IconLeftSampleWidget:
#         icon: root.icon
#
#
# <Example@FloatLayout>
#
#     BoxLayout:
#         orientation: 'vertical'
#
#         MDToolbar:
#             title: app.title
#             md_bg_color: app.theme_cls.primary_color
#             background_palette: 'Primary'
#             elevation: 10
#             left_action_items: [['menu', lambda x: x]]
#
#         MDScrollViewRefreshLayout:
#             id: refresh_layout
#             refresh_callback: app.refresh_callback
#             root_layout: root
#
#             MDGridLayout:
#                 id: box
#                 adaptive_height: True
#                 cols: 1
# ''')
#
#
# class IconLeftSampleWidget(ILeftBodyTouch, MDIconButton):
#     pass
#
#
# class ItemForList(OneLineIconListItem):
#     icon = StringProperty()
#
#
# class Example(MDApp):
#     title = 'Example Refresh Layout'
#     screen = None
#     x = 0
#     y = 15
#
#     def build(self):
#         self.screen = Factory.Example()
#         self.set_list()
#
#         return self.screen
#
#     def set_list(self):
#         async def set_list():
#             names_icons_list = list(md_icons.keys())[self.x:self.y]
#             for name_icon in names_icons_list:
#                 await asynckivy.sleep(0)
#                 self.screen.ids.box.add_widget(
#                     ItemForList(icon=name_icon, text=name_icon))
#         asynckivy.start(set_list())
#
#     def refresh_callback(self, *args):
#         '''A method that updates the state of your application
#         while the spinner remains on the screen.'''
#
#         def refresh_callback(interval):
#             self.screen.ids.box.clear_widgets()
#             if self.x == 0:
#                 self.x, self.y = 15, 30
#             else:
#                 self.x, self.y = 0, 15
#             self.set_list()
#             self.screen.ids.refresh_layout.refresh_done()
#             self.tick = 0
#
#         Clock.schedule_once(refresh_callback, 1)
#
#
# Example().run()

import csv


my_list1 = ["C1", ["a"], ["b"], ["c"], ["d"]]
my_list2 = ["C2", ["a"], ["b"], ["c"], ["d"]]
my_list3 = ["C3", ["a"], ["b"], ["c"], ["d"]]
my_list4 = ["C4", ["a"], ["b"], ["c"], ["d"]]
new_list = ["e"]


def set_data(filename, data_list):
    with open(filename, "a", newline="") as f:
        writer_object = csv.writer(f)
        writer_object.writerow(data_list)
        f.close()

def new_data(filename):
    with open(filename) as f:
        reader_obj = csv.reader(f)
        for i in reader_obj:
            if i[0] == "C1":
                return i

def add_data(filename):
    my_list = new_data("rough.csv")
    with open(filename, "a", newline="") as g:
        g.seek(0)
        for i in g:
            print(i)

add_data("rough.csv")



