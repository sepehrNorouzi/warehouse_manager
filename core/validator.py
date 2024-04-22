from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _


mobile_regex = RegexValidator(
    regex=r'^((?:[0-9]{8,10})|(?:\+[0-9][0-9]{11,14}))$',
    message=_(
        "Phone number must be entered in the format:+989999999999' or '99999999999'.Up to 13 digits allowed.allowed "
        "characters: [0-9] and '+'."))
