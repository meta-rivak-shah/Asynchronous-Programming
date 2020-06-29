from CommonApp.allvalidations import *
from CommonApp import constants

#  Validations for fields values taken from user input


class postValidations(object):
    _values = {
        "post_text": textValidator,
        "post_type": lambda required:choiceValidator(constants.POST_TYPE, required),
    }

    def __init__(self):
        self.__dict__ = self._values
