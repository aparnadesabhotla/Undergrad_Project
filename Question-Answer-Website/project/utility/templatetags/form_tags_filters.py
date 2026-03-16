from django import template

register = template.Library()


@register.filter(name = "label_suffix")
def set_label_suffix(field, suffix=''):
    field.field.label_suffix = suffix
    return field


@register.filter(name = "label")
def set_label(field, label='label'):
    field.label = label
    return field


@register.filter(name = "placeholder")
def set_placeholder(field, placeholder='placeholder'):
    field.field.widget.attrs.update({'placeholder': placeholder})
    return field