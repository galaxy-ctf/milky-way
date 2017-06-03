from django import template
from django.template.defaultfilters import stringfilter
from django.utils import timezone
from django.conf import settings
import re

register = template.Library()

@register.filter
@stringfilter
def redaction(value, user): # Only one argument.
    """Converts a string into all lowercase"""
    if settings.COMPETITION_STARTS < timezone.now() or user.is_superuser:
        return value
    return re.sub(r'[^\s]', '█', value)
