from django import template
from django.utils import timezone

register = template.Library()

@register.filter
def days_since(created_at):
    days = (timezone.now() - created_at).days
    return f"{days} days ago"