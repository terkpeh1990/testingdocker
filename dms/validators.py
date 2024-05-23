import os
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]  # Get the file extension
    valid_extensions = ['.pdf']

    if not ext.lower() in valid_extensions:
        raise ValidationError(_('File type is not supported. Please upload a PDF file.'))

