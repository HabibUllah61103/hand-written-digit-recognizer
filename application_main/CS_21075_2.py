import csv
from csv import writer
from abc import ABC, abstractmethod

class DataHandler(ABC):
    dialog = None
    shipping_dialog = None
    removal_dialog = None

    def set_id(self, filename=None):
        with open(filename) as f:
            id = f.readlines()
            ids = len(id)
            return ids

    def get_id(self, filename=None):
        data_list = []
        with open(filename) as f:
            reader_obj = csv.reader(f)
            for i in reader_obj:
                for j in i:
                    data_list.append(j)
            return data_list[0]

    def set_data(self, filename, data_list):
        with open(filename, "a", newline="") as f:
            writer_object = writer(f)
            writer_object.writerow(data_list)
            f.close()

    def data_collection(self, *args, credentials_filename=None, login_filename=None, user_id=None):
        signup_list = []
        login_list = [args[3].text, args[4].text]

        if credentials_filename == "admin_credentials.csv" and login_filename == "admin_login_credentials.csv":
            login_list.append(args[6].text)

        for credentials in args:
            if credentials.text == "":
                credentials.text = "-"
            signup_list.append(credentials.text)
        signup_list.insert(0, user_id)
        login_list.insert(0, user_id)
        self.set_data(credentials_filename, signup_list)
        self.set_data(login_filename, login_list)

    def verify(self, password, password_2):
        if password.text == "" and password_2.text == "":
            return False
        elif password_2.text == password.text:
            return True
        else:
            return False

    def show_dialog_box(self, **kwargs):
        pass

    def close_dialog(self, obj):
        self.dialog.dismiss()

    @abstractmethod
    def get_data(self, **kwargs):
        pass

    def validation(self, **kwargs):
        pass

    def get_cred(self, credential_list=None, email_address=None):
        self.info_list = None
        for i in credential_list:
            if i[1] == email_address.text:
                self.info_list = i
                break

        if self.info_list is None:
            self.show_dialog_box(title="Incorrect Email Address", text="Email Address is not found!!")
