# Imported files required to run the script
from kivy.config import Config

# These module functions will always be placed on top otherwise there properties won't execute.

Config.set("graphics", "width", "1080")
Config.set("graphics", "height", "640")
Config.set('graphics', 'resizable', False)
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen, ScreenManager
from CS_21076_2 import DataHandler
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivy.properties import ObjectProperty
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivy.factory import Factory
from kivymd.uix.textfield import MDTextField
from kivy.uix.gridlayout import GridLayout
from kivymd.uix.bottomsheet import MDCustomBottomSheet
from kivymd.uix.list import OneLineListItem, MDList, ThreeLineListItem
from kivymd.uix.filemanager import MDFileManager
from Final_Network import image_loader
import shutil
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
                self.dialog = MDDialog(title=title, text=text,
                                       buttons=[MDFlatButton(text="Close", on_release=self.close_dialog)])
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
                    self.show_dialog_box(title="Incorrect Password", text="Password is incorrect or does not filled!!")

        def set_current_user(self):
            user_list = self.info_list
            self.set_data(filename="current_user.csv", data_list=user_list)

    # This class displays signup screen of customer to user. Here user can register as a customer.
    class CustomerSignUp(Screen, DataHandler, metaclass=FinalMeta):
        def get_data(self, **kwargs):
            return None

        def show_dialog_box(self):
            if not self.dialog:
                self.dialog = MDDialog(title="Incorrect Passwords",
                                       text="Passwords are not filled or do not match. Please enter again!",
                                       buttons=[MDFlatButton(text="Close", on_release=self.close_dialog)])
            self.dialog.open()

        def set_id(self, filename="customer_credentials.csv"):
            self.customer_id = f"C{super().set_id(filename)}"
            return self.customer_id

        def data_saver(self, *args):
            self.data_collection(*args, credentials_filename="customer_credentials.csv",
                                 login_filename="customer_login_credentials.csv", user_id=self.set_id())

    # This class displays profile screen of customer. Here customer can see his credentials.
    class CustomerProfile(Screen, DataHandler, metaclass=FinalMeta):
        cred_list = ["Customer ID:", "Name:", "Email Address:", "Password:",
                     "Gender:", "Date of Birth:"]

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
            self.ids.customer_profile_info_grid.add_widget(MDLabel(text=f"{self.cred_list[0]} {self.data_list[0]}"))
            self.ids.customer_profile_info_grid.add_widget(
                MDLabel(text=f"{self.cred_list[1]} {self.data_list[1]} {self.data_list[2]} {self.data_list[3]}"))
            for i in range(2, len(self.cred_list)):
                self.ids.customer_profile_info_grid.add_widget(
                    MDLabel(text=f"{self.cred_list[i]} {self.data_list[i + 2]}"))

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
            self.file_manager = MDFileManager(
                exit_manager=self.exit_file_manager,
                select_path=self.select_path,   
            )
            self.file_manager.show("/")

        def exit_file_manager(self, *args):
            # Callback for when the user exits the file manager
            self.file_manager.close()

        def select_path(self, path):
            with open('current_user.csv', 'r') as current_user:
                csv_reader = csv.reader(current_user)
                for row in csv_reader:
                    current_user = row[2]

            if not(current_user in os.listdir("./output")):
                os.chdir("./output")
                os.mkdir(current_user)
                os.chdir("../")
            
            destination_folder = './output/'+str(current_user) + '/'

            try:
                image_loader(path, destination_folder)
                self.exit_file_manager()
            except Exception as e:
                print(f"Error: {e}")

    # This class is used to extend properties of MDCard class, and develop the better variant of display cards to show our products.
    class ElementCard(MDCard, DataHandler, metaclass=FinalMeta):
        quantity_list = ObjectProperty(None)

        def get_data(self, obj, filename=None):
            data_list = []
            with open(filename) as f:
                reader_obj = csv.reader(f)
                for i in reader_obj:
                    data_list.append(i[0])
                index = data_list.index(obj.prod_id)
                f.close()

            with open(filename) as f:
                data = csv.reader(f)
                for i in range(index):
                    next(data)
                laptop_data = next(data)
                f.close()

            check_string = f"""
Manufacturing Company: {laptop_data[5]}\n
Display Size: {laptop_data[6]}\n
CPU: {laptop_data[7]}\n
RAM Memory: {laptop_data[8]}\n
Hard Disk Memory: {laptop_data[9]}\n
GPU: {laptop_data[10]}\n
Battery: {laptop_data[11]}\n
Operating System: {laptop_data[12]}\n
Weight: {laptop_data[13]}\n
Color: {laptop_data[14]}\n"""

            self.dialog = MDDialog(title='Specifications', text=check_string, size_hint=(0.5, 0.25), buttons=[
                MDFlatButton(text='Close',
                             on_release=self.close_dialog)])
            self.dialog.open()

        def show_sheet(self):
            self.my_list = MDList()
            my_sheet = Factory.ContentCustomSheet()
            for i in range(1, 21):
                items = OneLineListItem(
                    text=f"                                                                                                                                 {i}",
                    on_release=self.confirmation)
                self.my_list.add_widget(items)
            my_sheet.ids.product_quantity_list.add_widget(self.my_list)
            self.custom_sheet = MDCustomBottomSheet(screen=my_sheet)
            self.custom_sheet.open()

        def close_dialog(self, obj):
            self.confirm_dialog.dismiss()

        def confirmation(self, obj):
            self.product_quantity = obj.text.strip()

            self.confirm_dialog = MDDialog(title="Order Confirmed!!", text="Item added to cart successfully",
                                           size_hint=(0.3, 0.1),
                                           buttons=[MDFlatButton(text='Close', on_release=self.close_dialog)])
            self.confirm_dialog.open()

            self.datalist = [self.prod_id, self.laptop_name, self.price, self.product_quantity]
            self.add_to_cart()

        def add_to_cart(self):
            user_id = self.get_id(filename="current_user.csv")
            cart_filename = f"{user_id}_current_cart.csv"
            self.set_data(filename=cart_filename, data_list=self.datalist)

    # This class is used to display order quantity sheet for the selection of order quantity.
    class ContentCustomSheet(GridLayout):
        pass

    # This class displays shopping cart screen of customer. Here user can see all his orders, remove them,
    # as well as check them out for completion of purchase processes.
    class CurrentCart(Screen, DataHandler, metaclass=FinalMeta):
        def on_pre_enter(self, *args, filename=None):
            while True:
                try:
                    self.user_id = self.get_id("current_user.csv")
                    self.cart_filename = f"{self.user_id}_current_cart.csv"

                    with open(self.cart_filename) as f:
                        file_data = f.read()
                        if file_data == "":
                            self.empty_note = MDLabel(text='Cart is empty', halign="center")
                            self.ids.customer_current_cart_info.add_widget(self.empty_note)
                            f.close()
                        else:
                            with open(self.cart_filename) as data:
                                reader_obj = csv.reader(data)
                                self.label = MDLabel(text="Click the item to remove it from cart",
                                                     halign='center')
                                self.ids.customer_current_cart_info.add_widget(self.label)
                                for i in reader_obj:
                                    self.items = ThreeLineListItem(text=i[1], secondary_text=i[2],
                                                                   tertiary_text=f"{i[3]} items",
                                                                   on_release=self.open_dialog)
                                    self.ids.customer_current_cart_info.add_widget(self.items)
                        break

                except FileNotFoundError as e:
                    with open(self.cart_filename, "w") as f:
                        f.close()

        def open_dialog(self, obj):
            self.address = obj

            self.removal_dialog = MDDialog(title='Confirmation', text='Do you want to remove this item?',
                                           buttons=[MDFlatButton(text='No', on_release=self.close_removal_dialog),
                                                    MDFlatButton(text='Yes', on_release=self.remove_item)])
            self.removal_dialog.open()

        def remove_item(self, obj):
            self.ids.customer_current_cart_info.remove_widget(self.address)
            self.order_list = []
            with open(self.cart_filename) as f:
                reader_obj = csv.reader(f)
                for i in reader_obj:
                    self.order_list.append(i)
                    for item in i:
                        if item == self.address.text:
                            self.order_list.remove(i)
            self.removal_dialog.dismiss()

            with open(self.cart_filename, "w", newline="") as f:
                writer_obj = csv.writer(f)
                for i in self.order_list:
                    writer_obj.writerow(i)

        def shipping_info(self, obj):
            self.shipping_dialog = MDDialog(title='Shipping Address',
                                            buttons=[MDFlatButton(text='Close', on_release=self.close_shipping_dialog),
                                                     MDFlatButton(text='Next', on_release=self.checkout)],
                                            size_hint=(0.4, 0.9))

            self.ship_address = MDTextField(hint_text='Enter your Shipping Address',
                                            helper_text='It is necessary for order placement',
                                            helper_text_mode='on_focus',
                                            pos_hint={'center_x': 0.5, 'center_y': 0.5}, size_hint_x=None, height=50,
                                            width=350)
            self.shipping_dialog.add_widget(self.ship_address)
            self.shipping_dialog.open()

        def checkout(self, obj):
            self.shipping_dialog.dismiss()
            self.string = '* Select Payment Method\n\n\n\n'
            self.checkout_dialog = MDDialog(text=self.string, size_hint=(0.3, 1),
                                            buttons=[MDFlatButton(text='close', on_release=self.close_dialog)])
            self.payment_method = MDList()
            self.cash_on_delivery = OneLineListItem(text='Cash on Delivery', on_release=self.final_dialog)
            self.credit_card = OneLineListItem(text='Credit Card', on_release=self.final_dialog)
            self.payment_method.add_widget(self.cash_on_delivery)
            self.payment_method.add_widget(self.credit_card)
            self.checkout_dialog.add_widget(self.payment_method)
            self.checkout_dialog.open()

        def get_data(self, filename=None):
            data_list = []
            with open(filename) as f:
                reader_obj = csv.reader(f)
                for i in reader_obj:
                    data_list.append(i)
                return data_list

        def final_dialog(self, obj):
            self.checkout_dialog.dismiss()
            self.placement_dialog = MDDialog(title='Order Placed', text='Thank You for Shopping.\nHave a Blessed Day!!',
                                             size_hint=(0.3, 1),
                                             buttons=[
                                                 MDFlatButton(text='Finish', on_release=self.close_placement_dialog)])
            self.placement_dialog.open()

            self.shopping_history_filename = f"{self.user_id}_shopping_history.csv"
            with open(self.shopping_history_filename, "a", newline="") as f:
                writer_obj = csv.writer(f)
                orders_data = self.get_data(filename=self.cart_filename)
                for i in orders_data:
                    writer_obj.writerow(i)

            with open(self.cart_filename, "w") as f:
                f.close()

        def close_removal_dialog(self, obj):
            self.removal_dialog.dismiss()

        def close_shipping_dialog(self, obj):
            self.shipping_dialog.dismiss()

        def close_placement_dialog(self, obj):
            self.placement_dialog.dismiss()
            self.ids.customer_current_cart_info.clear_widgets()

        def on_pre_leave(self, *args):
            self.ids.customer_current_cart_info.clear_widgets()

    # This class displays complete shopping history of customer.
    class ShoppingHistory(Screen, DataHandler, metaclass=FinalMeta):
        def get_data(self, **kwargs):
            return None

        def on_pre_enter(self, *args):
            while True:
                try:
                    self.user_id = self.get_id(filename="current_user.csv")
                    self.shopping_history_filename = f"{self.user_id}_shopping_history.csv"

                    with open(self.shopping_history_filename) as f:
                        file_data = f.read()
                        if file_data == "":
                            self.empty_note = MDLabel(text='No Response History', halign="center")
                            self.ids.customer_shopping_history_list.add_widget(self.empty_note)
                            f.close()
                        else:
                            with open(self.shopping_history_filename) as data:
                                reader_obj = csv.reader(data)
                                for i in reader_obj:
                                    self.items = ThreeLineListItem(text=i[1], secondary_text=i[2],
                                                                   tertiary_text=f"{i[3]} items")
                                    self.ids.customer_shopping_history_list.add_widget(self.items)
                    break

                except FileNotFoundError as e:
                    with open(self.shopping_history_filename, "w") as f:
                        f.close()

        def on_leave(self, *args):
            self.ids.customer_shopping_history_list.clear_widgets()

    # This class displays login screen of administrator. Here administrator can sign in to application.
    class AdminLogin(Screen, DataHandler, metaclass=FinalMeta):
        with open("current_admin.csv", "w") as f:
            f.close()

        def show_dialog_box(self, title=None, text=None):
            self.dialog = None
            if not self.dialog:
                self.dialog = MDDialog(title=title, text=text,
                                       buttons=[MDFlatButton(text="Close", on_release=self.close_dialog)])
            self.dialog.open()

        def get_data(self, filename=None):
            data_list = []
            with open(filename) as f:
                reader_obj = csv.reader(f)
                for i in reader_obj:
                    data_list.append(i)
            return data_list

        def validation(self, email=None, pswd=None, sec_code=None):
            cred_list = self.get_data(filename="admin_login_credentials.csv")
            self.get_cred(credential_list=cred_list, email_address=email)

            if self.info_list is not None:
                if self.info_list[2] == pswd.text:
                    if self.info_list[3] == sec_code.text:
                        self.ids.admin_login_login_email_textfield.text = ""
                        self.ids.admin_login_login_pswd_textfield.text = ""
                        self.ids.admin_login_login_security_code_textfield.text = ""
                        self.set_current_admin()
                        return True
                    else:
                        self.show_dialog_box(title="Incorrect Security Code",
                                             text="Security Code does not match with given Email Address!!")
                else:
                    self.show_dialog_box(title="Incorrect Password", text="Password is incorrect or does not filled!!")

        def set_current_admin(self):
            user_list = self.info_list
            self.set_data(filename="current_admin.csv", data_list=user_list)

    # This class displays signup screen of administrator to user. Here user can register as an administrator.
    class AdminSignUp(Screen, DataHandler, metaclass=FinalMeta):
        def get_data(self, **kwargs):
            return None

        def set_id(self, filename="admin_credentials.csv"):
            self.customer_id = f"A{super().set_id(filename)}"
            return self.customer_id

        def data_saver(self, *args):
            self.data_collection(*args, credentials_filename="admin_credentials.csv",
                                 login_filename="admin_login_credentials.csv", user_id=self.set_id())

    # This class displays action screen of administrator. Here administrator can see various actions he can perform, regarding the application.
    class Admin(Screen):
        def logout(self, filename):
            with open(filename, "w") as f:
                f.close()

    # This class displays profile screen of customer. Here customer can see his credentials.
    class AdminProfile(Screen, DataHandler, metaclass=FinalMeta):
        def get_data(self, filename=None):
            self.user_id = self.get_id(filename="current_admin.csv")
            with open(filename) as f:
                reader_obj = csv.reader(f)
                for i in reader_obj:
                    if i[0] == self.user_id:
                        return i

        cred_list = ["Administrator ID:", "Name:", "Email Address:", "Password:", "Phone Number:", "Security Code:",
                     "Designation:", "Field Department:", "Department ID:", "Credit Card Number:",
                     "Gender:", "Date of Birth:", "Nationality:"]

        def gen_grid(self, *args):
            self.data_list = self.get_data(filename="admin_credentials.csv")
            if self.data_list[2] == "-":
                self.data_list[2] = ""
            if self.data_list[3] == "-":
                self.data_list[3] = ""
            self.ids.admin_profile_info_grids.add_widget(MDLabel(text=f"{self.cred_list[0]} {self.data_list[0]}"))
            self.ids.admin_profile_info_grids.add_widget(
                MDLabel(text=f"{self.cred_list[1]} {self.data_list[1]} {self.data_list[2]} {self.data_list[3]}"))
            for i in range(2, len(self.cred_list)):
                self.ids.admin_profile_info_grids.add_widget(
                    MDLabel(text=f"{self.cred_list[i]} {self.data_list[i + 2]}"))

        def on_pre_enter(self, *args):
            self.gen_grid()

        def on_pre_leave(self, *args):
            self.ids.admin_profile_info_grids.clear_widgets()

    # This class displays profile screen of customer to administrator. Here administrator can see the customer's credentials.
    class AdminCustomerInfo(Screen, DataHandler, metaclass=FinalMeta):
        def get_data(self, filename=None):
            ids_list = []
            with open(filename) as f:
                reader_obj = csv.reader(f)
                for i in reader_obj:
                    ids_list.append(i[0])
                return ids_list

        def on_pre_enter(self, *args):
            id_list = self.get_data(filename="customer_credentials.csv")
            for i in id_list:
                my_list = OneLineListItem(text=f"{i}", on_release=self.show_user_dialog)
                self.ids.admin_customer_info_list.add_widget(my_list)

        def get_user(self, filename=None):
            with open(filename) as f:
                reader_obj = csv.reader(f)
                for i in reader_obj:
                    if i[0] == self.user_id:
                        return i

        def show_user_dialog(self, obj):
            self.user_id = obj.text
            self.user = self.get_user(filename="customer_credentials.csv")
            print(self.user)
            cred_list = ["Customer ID:", "Name:", "Email Address:", "Password:", "Phone Number:", "Credit Card Number:",
                         "Gender:", "Date of Birth:"]

            if self.user[2] == "-":
                self.user[2] = ""
            if self.user[3] == "-":
                self.user[3] = ""

            check_string = f"""
{cred_list[0]} {self.user[0]}\n
{cred_list[1]} {self.user[1]} {self.user[2]} {self.user[3]}\n
{cred_list[2]} {self.user[4]}\n
{cred_list[3]} {self.user[5]}\n
{cred_list[4]} {self.user[6]}\n
{cred_list[5]} {self.user[7]}\n
{cred_list[6]} {self.user[8]}\n
{cred_list[7]} {self.user[9]}\n
"""
            self.my_user_dialog = MDDialog(title="Customer Information", text=check_string,
                                           buttons=[MDFlatButton(text="Close", on_release=self.close_user_dialog)])
            self.my_user_dialog.open()

        def close_user_dialog(self, obj):
            self.my_user_dialog.dismiss()

        def on_pre_leave(self, *args):
            self.ids.admin_customer_info_list.clear_widgets()

    # This class displays product screen to administrator. Here administrator can update stock as well as perform different actions regarding products.
    class AdminProductView(Screen, DataHandler, metaclass=FinalMeta):
        selected_file_path = ""
        def get_data(self, filename=None):
            ids_list = []
            with open(filename) as f:
                reader_obj = csv.reader(f)
                for i in reader_obj:
                    ids_list.append(i[0])
                return ids_list

        def open_file_manager(self):
            file_manager = MDFileManager(
                exit_manager=self.exit_file_manager,
                select_path=self.select_path,
            )
            file_manager.show('/')

        def exit_file_manager(self, *args):
            # Callback for when the user exits the file manager
            pass

        def select_path(self, path):
            # Callback for when a file is selected in the file manager
            print(f"Selected file: {path}")
            
            # Specify the destination folder where you want to move the file
            destination_folder = '/path/to/your/destination/folder'

            try:
                # Move or copy the selected file to the destination folder
                shutil.move(path, destination_folder)
                # If you want to copy instead of move, use shutil.copy instead of shutil.move

                print(f"File moved to: {destination_folder}")
            except Exception as e:
                print(f"Error: {e}")

#         def on_pre_enter(self, *args):
#             id_list = self.get_data(filename="products_info.csv")
#             for i in id_list:
#                 my_list = OneLineListItem(text=f"{i}", on_release=self.show_product_dialog)
#                 self.ids.admin_product_info_list.add_widget(my_list)

#         def get_product(self, filename=None):
#             with open(filename) as f:
#                 reader_obj = csv.reader(f)
#                 for i in reader_obj:
#                     if i[0] == self.product_id:
#                         return i

#         def show_product_dialog(self, obj):
#             self.product_id = obj.text
#             self.product = self.get_product(filename="products_info.csv")
#             cred_list = ["Product ID:", "Rating:", "Price:", "Name:", "Manufacturing Company:", "Screen Size:",
#                          "Processor:", "RAM Memory:", "Hard Drive Memory:", "GPU:", "Battery:",
#                          "Weight:", "Color:"]

#             check_string = f"""
# {cred_list[0]} {self.product[0]}                               {cred_list[1]} {self.product[2]}                            {cred_list[2]} {self.product[3]}\n
# {cred_list[3]} {self.product[4]}\n
# {cred_list[4]} {self.product[5]}\n
# {cred_list[5]} {self.product[6]}\n
# {cred_list[6]} {self.product[7]}\n
# {cred_list[7]} {self.product[8]}                                  {cred_list[8]} {self.product[9]}\n
# {cred_list[9]} {self.product[10]}\n
# {cred_list[10]} {self.product[11]}\n
# {cred_list[11]} {self.product[13]}                                          {cred_list[12]} {self.product[14]}\n
# """
#             self.my_product_dialog = MDDialog(title="Product Information", text=check_string, size_hint=(0.6, .6),
#                                               buttons=[MDFlatButton(text="Close",
#                                                                     on_release=self.close_product_dialog)])
#             self.my_product_dialog.open()

#         def close_product_dialog(self, obj):
#             self.my_product_dialog.dismiss()

#         def on_pre_leave(self, *args):
#             self.ids.admin_product_info_list.clear_widgets()

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
