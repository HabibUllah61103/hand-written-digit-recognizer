# Imported files required to run the script
from kivy.config import Config

# These module functions will always be placed on top otherwise there properties won't execute.

Config.set("graphics", "width", "1080")
Config.set("graphics", "height", "640")
Config.set("graphics", "resizable", False)
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen, ScreenManager
from CS_21076_2 import DataHandler
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivy.uix.gridlayout import GridLayout
from kivymd.uix.list import ThreeLineListItem
from kivymd.uix.filemanager import MDFileManager
from kivy.uix.image import Image
from Final_Network import image_loader
import csv
import os


class FinalMeta(type(DataHandler), type(Screen)):
    pass


# The main container class developed to provide the single interface to all contained classes.
class GUI:
    # This class displays introduction screen of  application.
    class Intro(Screen):
        pass

    # This class displays login screen of customer. Here customer can sign in to application.
    class CustomerLogin(Screen, DataHandler, metaclass=FinalMeta):
        with open("current_user.csv", "w") as f:
            f.close()

        def show_dialog_box(self, title=None, text=None):
            self.dialog = None
            if not self.dialog:
                self.dialog = MDDialog(
                    title=title,
                    text=text,
                    buttons=[MDFlatButton(text="Close", on_release=self.close_dialog)],
                )
            self.dialog.open()

        def get_data(self, filename=None, email=None):
            data_list = []
            with open(filename) as f:
                reader_obj = csv.reader(f)
                for i in reader_obj:
                    data_list.append(i)
            return data_list

        def validation(self, email=None, pswd=None):
            cred_list = self.get_data(filename="customer_login_credentials.csv")
            self.get_cred(credential_list=cred_list, email_address=email)

            if self.info_list is not None:
                if self.info_list[2] == pswd.text:
                    self.ids.customer_login_login_email_textfield.text = ""
                    self.ids.customer_login_login_pswd_textfield.text = ""
                    self.set_current_user()
                    return True
                else:
                    self.show_dialog_box(
                        title="Incorrect Password",
                        text="Password is incorrect or does not filled!!",
                    )

        def set_current_user(self):
            user_list = self.info_list
            self.set_data(filename="current_user.csv", data_list=user_list)

    # This class displays signup screen of customer to user. Here user can register as a customer.
    class CustomerSignUp(Screen, DataHandler, metaclass=FinalMeta):
        def get_data(self, **kwargs):
            return None

        def show_dialog_box(self):
            if not self.dialog:
                self.dialog = MDDialog(
                    title="Incorrect Passwords",
                    text="Passwords are not filled or do not match. Please enter again!",
                    buttons=[MDFlatButton(text="Close", on_release=self.close_dialog)],
                )
            self.dialog.open()

        def set_id(self, filename="customer_credentials.csv"):
            self.customer_id = f"C{super().set_id(filename)}"
            return self.customer_id

        def data_saver(self, *args):
            self.data_collection(
                *args,
                credentials_filename="customer_credentials.csv",
                login_filename="customer_login_credentials.csv",
                user_id=self.set_id(),
            )

    # This class displays profile screen of customer. Here customer can see his credentials.
    class CustomerProfile(Screen, DataHandler, metaclass=FinalMeta):
        cred_list = [
            "Customer ID:",
            "Name:",
            "Email Address:",
            "Password:",
        ]

        def get_data(self, filename=None):
            self.user_id = self.get_id(filename="current_user.csv")
            with open(filename) as f:
                reader_obj = csv.reader(f)
                for i in reader_obj:
                    if i[0] == self.user_id:
                        return i

        def gen_grid(self):
            self.data_list = self.get_data(filename="customer_credentials.csv")
            if self.data_list[2] == "-":
                self.data_list[2] = ""
            if self.data_list[3] == "-":
                self.data_list[3] = ""
            self.ids.customer_profile_info_grid.add_widget(
                MDLabel(text=f"{self.cred_list[0]} {self.data_list[0]}")
            )
            self.ids.customer_profile_info_grid.add_widget(
                MDLabel(
                    text=f"{self.cred_list[1]} {self.data_list[1]} {self.data_list[2]} {self.data_list[3]}"
                )
            )
            for i in range(2, len(self.cred_list)):
                self.ids.customer_profile_info_grid.add_widget(
                    MDLabel(text=f"{self.cred_list[i]} {self.data_list[i + 2]}")
                )

        def on_pre_enter(self, *args):
            self.gen_grid()

        def on_leave(self):
            self.ids.customer_profile_info_grid.clear_widgets()

    # This class displays product screen to customer. Here customer can view and add the products to his cart.
    class Product(Screen):
        selected_file_path = ""

        def logout(self, filename=None):
            with open(filename, "w") as f:
                f.close()

        def open_file_manager(self):
            initial_path = os.getcwd()
            self.file_manager = MDFileManager(
                exit_manager=self.exit_file_manager,
                select_path=self.select_path,
            )
            self.file_manager.show(initial_path)

        def exit_file_manager(self, *args):
            # Callback for when the user exits the file manager
            self.file_manager.close()

        def select_path(self, path):
            with open("current_user.csv", "r") as current_user:
                csv_reader = csv.reader(current_user)
                for row in csv_reader:
                    current_user = row[2]
                    current_user_id = row[0]

            if not (current_user in os.listdir("./output")):
                os.chdir("./output")
                os.mkdir(current_user)
                os.chdir("../")

            destination_folder = "./output/" + str(current_user) + "/"

            try:
                current_image_path, output, current_time = image_loader(
                    path, destination_folder
                )
                self.exit_file_manager()
                # Clear existing image widgets before adding a new one
                self.ids.image_display_layout.clear_widgets()
                self.ids.output_button.clear_widgets()

                # Create an MDImage widget to display the loaded image
                image_widget = Image(source=current_image_path, size_hint=(1, 1))
                temp = "Predicted Output: " + str(output)

                self.shopping_history_filename = (
                    f"{current_user_id}_shopping_history.csv"
                )
                with open(self.shopping_history_filename, "a", newline="") as f:
                    writer_obj = csv.writer(f)
                    orders_data = [[current_time, current_image_path, output]]
                    for i in orders_data:
                        writer_obj.writerow(i)

                # Add the image widget to the screen
                self.ids.output_button.text = temp
                self.ids.image_display_layout.add_widget(image_widget)

            except Exception as e:
                print(f"Error: {e}")

    # This class is used to display order quantity sheet for the selection of order quantity.
    class ContentCustomSheet(GridLayout):
        pass

    # This class displays complete shopping history of customer.
    class ShoppingHistory(Screen, DataHandler, metaclass=FinalMeta):
        def get_data(self, **kwargs):
            return None

        def on_pre_enter(self, *args):
            while True:
                try:
                    self.user_id = self.get_id(filename="current_user.csv")
                    self.shopping_history_filename = (
                        f"{self.user_id}_shopping_history.csv"
                    )

                    with open(self.shopping_history_filename) as f:
                        file_data = f.read()
                        if file_data == "":
                            self.empty_note = MDLabel(
                                text="No Response History", halign="center"
                            )
                            self.ids.customer_shopping_history_list.add_widget(
                                self.empty_note
                            )
                            f.close()
                        else:
                            with open(self.shopping_history_filename) as data:
                                reader_obj = csv.reader(data)
                                for i in reader_obj:
                                    self.items = ThreeLineListItem(
                                        text=f"Predicted Output: {i[2]}",
                                        secondary_text=f"Saved Image Path: {i[1]}",
                                        tertiary_text=f"Date & Time: {i[0]}",
                                    )
                                    self.ids.customer_shopping_history_list.add_widget(
                                        self.items
                                    )
                    break

                except FileNotFoundError as e:
                    with open(self.shopping_history_filename, "w") as f:
                        f.close()

        def on_leave(self, *args):
            self.ids.customer_shopping_history_list.clear_widgets()

    # This class manages the flow, as well as transitions between different screens.
    class Manager(ScreenManager):
        def callback(self, screen, direction):
            self.current = screen
            self.transition.direction = direction

    # This class is used to build and initiate the application.
    class ShoppingApp(MDApp):
        def build(self):
            kv = Builder.load_file("CS_21076_1.kv")
            return kv

        def on_start(self):
            self.title = "Handwritten Digit Recognator (HDAAAI)"


app = GUI().ShoppingApp().run()
