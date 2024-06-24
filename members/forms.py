
from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.utils.translation import gettext_lazy as _

from .models import Member


class UserUpdateForm(UserChangeForm):
    class Meta:
        model = Member
        fields = ['phone']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            ctx = {
                'placeholder': self.fields[field].label or _(field.title()),
            }
            self.fields[field].widget.attrs.update(ctx)


