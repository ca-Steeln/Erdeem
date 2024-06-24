
from django import forms
from django.forms import widgets

class Widget(forms.widgets.ChoiceWidget):
    """
    Subclass of Django's select widget that allows disabling options.
    """
    def __init__(self, disabled_choices=None, *args, **kwargs):
        super(Widget, self).__init__(*args, **kwargs)
        self.disabled_choices = disabled_choices

    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option_dict = super().create_option(
            name, value, label, selected, index, subindex=subindex, attrs=attrs
        )

        if self.disabled_choices and value in self.disabled_choices:
            option_dict['attrs']['disabled'] = 'disabled'
            option_dict['attrs']['title'] = 'This item is currently unavailable'
        return option_dict

class SelectWidget(Widget, forms.Select):
    pass

class RadioSelectWidget(Widget, forms.RadioSelect):
    pass