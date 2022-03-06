from typing import Type
import os
import json
import logging
from dataclasses import dataclass
import enum

logging.basicConfig(
    level=logging.DEBUG,
    format="[%(levelname)s] => `%(message)s` @ %(asctime)s"
)

logger = logging.getLogger(__name__)
logger.info("Logger is initialized...")


class Gender(enum.Enum):
    """
    Enumeration to specify the `User`
    gender.
    """
    not_specified = 0
    male = 1
    female = 2


# TODO: Find a way to refactor classes that user
# JSON to use this mixin
class JSONFeatureMixin:
    def load(self):
        try:
            with open(self.filename, 'r') as file:
                self.data = json.loads(file.read())
                self._postprocess_for_load()
        except FileNotFoundError:
            with open(self.filename, 'w') as file:
                file.write(json.dumps(self._file_default_content))
                self.data = self._file_default_content
                self._postprocess_for_load()
        except Exception as e:
            raise(e)

    def save(self):
        self._preprocess_for_save()
        with open(self.filename, 'w') as file:
            file.write(json.dumps(self.data))

    def delete(self):
        os.remove(self.filename)


@dataclass
class User:
    """
    This class models the user and
    holds the user data
    """
    firstname: str
    lastname: str
    email: str
    gender: Gender

    def fullname(self, order: str = 'lf') -> str:
        """
        Returns the user fullname.
        order specifies how the name
        should be returned.
        lf = lastname before firstname
        fl = firstname befor lastname
        """
        if order == 'lf':
            return f'{self.lastname} {self.firstname}'
        elif order == 'fl':
            return f'{self.firstname} {self.lastname}'
        return None

    def __repr__(self) -> str:
        return f"User: {self.email}"

    def __eq__(self, __o: object) -> bool:
        self.firstname == __o.firstname & self.lastname == __o.lastname & self.email == __o.email

    def serialize(self) -> dict:
        """
        Converts instance to a dictionary
        that is serializable by JSON
        """
        default = {
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email
        }

        gender = 0
        if self.gender == Gender.male:
            gender = 1
        elif self.gender == Gender.female:
            gender = 2

        default['gender'] = gender
        return default

    @classmethod
    def deserialize(cls, value_dict: dict):
        gender = value_dict['gender']
        gender_value = Gender.not_specified
        if gender == 1:
            gender_value = Gender.male
        elif gender == 2:
            gender_value = Gender.female

        return cls(firstname=value_dict['firstname'], lastname=value_dict['lastname'], email=value_dict['email'], gender=gender_value)


# TODO: Fix error that might occure in parsing template file to json
# jinja2 template engine users curly braces {{}} which may confuse the
# json parser.
@dataclass
class MailTemplate:
    """
    Holds the template info if the
    user decides to save it
    """
    name: str
    template: str

    def serialize(self) -> dict:
        """
        converts the `Mail` instance
        to a dictionary that JSON
        can work with.
        """
        return {
            'name': self.name,
            'template': self.template
        }

    @classmethod
    def deserialize(cls, value_dict: dict):
        """
        creates a `Mail` instance from the
        `value_dict` provided
        """
        pass

    def render(self, data: dict) -> str:
        """
        Renders the mail template based on the 
        data provided.
        """
        pass

    def __repr__(self) -> str:
        return f"Mail: {self.name}"

    def __eq__(self, __o: object) -> bool:
        self.name == __o.name & self.template == __o.template


class MailTemplateBook(JSONFeatureMixin):
    def __init__(self) -> None:
        self.filename = '.mail_templates.json'
        self._file_default_content = []
        self.load()

    def _preprocess_for_save(self):
        self.data = [template.serialize()
                     for template in self.mail_template_list]

    def _postprocess_for_load(self):
        self.mail_template_list = [MailTemplate(
            template['name'], template['template']) for template in self.data]

    def add_template(self, name: str, template: str):
        self.mail_template_list.append(MailTemplate(name, template))
        self.save()


class AddressBook(JSONFeatureMixin):
    """
    This model handels all the
    functionality required to 
    managing the user contacts
    """

    def __init__(self, filename: str = '.default_contacts.json'):
        self.filename = filename
        self._file_default_content = []
        self._contact_list = []
        self.load()

    def add_contact(self, firstname: str, lastname: str, email: str, gender: str = None):
        new_user = User(firstname, lastname, email, gender)
        self.contact_list.append(new_user)
        self.save()

    @property
    def contact_list(self):
        return self._contact_list

    def _postprocess_for_load(self):
        """
        Loads the contacts from the file
        """

        # create an instance of the gender enum that matches the user gender in the file
        for user in self.data:
            if user['gender'] == 0:
                user['gender'] = Gender.not_specified
            elif user['gender'] == 1:
                user['gender'] = Gender.male
            elif user['gender'] == 2:
                user['gender'] = Gender.female

            # create a User model instance
            user = User.deserialize(user)
            # add User instance to the contact list
            self.contact_list.append(user)

    def _preprocess_for_save(self):
        self.data = [user.serialize() for user in self._contact_list]


class Setting(JSONFeatureMixin):
    """
    Model for handling settings
    for the application
    """

    def __init__(self, filename: str = '.settings.json') -> None:
        self.filename = filename
        self._file_default_content = {}
        self.load()

    def _postprocess_for_load(self):
        self._settings = self.data

    def _preprocess_for_save(self):
        self.data = self._settings

    @property
    def settings(self):
        return self._settings

    def _generate_default_settings(self):
        """
        Creates the default settings
        """
        pass

    def update_setting(self, config_name: str, value: str):
        config = self._settings.get(config_name, None)
        if config is None:
            self._settings = self._settings | {config_name: value}
        else:
            self._settings[config_name] = value

        self.save()

    def get_config(self, config_name) -> str:
        """
        Returns the configuration value of a 
        settings.
        """
        return self._settings.get(config_name, None)


class Pizza:
    """
    Core Email functionality
    """

    def __init__(self, address_book: AddressBook, settings: Setting) -> None:
        self._from = ""
        self.to = None
        self.template = ""
        self.address_book = address_book
        self.settings = settings

    def sendmail(self):
        pass

    def add_recipient_all(self):
        pass

    def add_recipient_bulk(self):
        pass

    def add_recipient(self):
        pass

    def render(self):
        pass
