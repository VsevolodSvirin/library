from django.core.exceptions import ValidationError
from django.forms import CharField


class StrictCharField(CharField):

    def to_python(self, value):
        if isinstance(value, str):
            return super().to_python(value)

        raise ValidationError('String is required')

