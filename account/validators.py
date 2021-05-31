import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class NumberValidator(object):
    def __init__(self, min_digits=1):
        self.min_digits = min_digits

    def validate(self, password, user=None):
        if not len(re.findall('\d', password)) >= self.min_digits:
            raise ValidationError(
                message=f"A senha deve conter pelo menos {self.min_digits} dígito(s), 0-9.",
                params={'min_digits': self.min_digits},
            )

    def get_help_text(self):
        return f"Sua senha deve conter pelo menos {self.min_digits} dígito(s), 0-9."


class UppercaseValidator(object):
    def validate(self, password, user=None):
        if not re.findall('[A-Z]', password):
            raise ValidationError(
                message=f"A senha deve conter pelo menos 1 letra maiúscula, A-Z.",
                code='password_no_upper',
            )

    def get_help_text(self):
        return _(
            "Sua senha deve conter pelo menos 1 letra maiúscula, A-Z."
        )


class LowercaseValidator(object):
    def validate(self, password, user=None):
        if not re.findall('[a-z]', password):
            raise ValidationError(
                message=f"A senha deve conter pelo menos 1 letra maiúscula, a-z.",
                code='password_no_lower',
            )

    def get_help_text(self):
        return _(
            "Sua senha deve conter pelo menos 1 letra minúscula, a-z."
        )


class SymbolValidator(object):
    def validate(self, password, user=None):
        if not re.findall('[()[\]{}|\\`~!@#$%^&*_\-+=;:\'",<>./?]', password):
            raise ValidationError(
                _("A senha deve conter pelo menos 1 caractere especial."))

    def get_help_text(self):
        return _(
            "Sua senha deve conter pelo menos 1 caractere especial." +
            " ()[]{}|\`~!@#$%^&*_-+=;:'\",<>./?"
        )
