from CommonApp.allvalidations import *
from CommonApp.constants import *


#  Validations for fields values taken from user input
class userValidations(object):
    _values = {
        "first_name": personNameValidator,
        "last_name": personNameValidator,
        "email": emailValidator,
        "password1": passwordValidator,
        "password2": passwordValidator,
    }

    def __init__(self):
        self.__dict__ = self._values
