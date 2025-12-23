from django.template import Library

register = Library()

@register.simple_tag
def display_time(time):

    return f'{time.hour}h {time.minute}m'