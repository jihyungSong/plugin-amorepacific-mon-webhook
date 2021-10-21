from spaceone.core.error import *


class ERROR_CHECK_VALIDITY(ERROR_BASE):
    _message = 'Event model is not validate (field= {field})'


class ERROR_REQUIRED_FIELDS(ERROR_BASE):
    _message = 'Required field is missing(field= {field})'

