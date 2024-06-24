
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from allauth.account.forms import LoginForm, SignupForm

from recaptcha.forms import ReCaptchaV3Field

class RegistrationForm(SignupForm):
    recaptcha = ReCaptchaV3Field(action='signup')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:

            self.fields[field].label = ''
            self.fields[field].help_text = None

    def save(self, request):
        user = super(RegistrationForm, self).save(request)

        # Add your own processing here.

        return user


class AuthenticationForm(LoginForm):
    recaptcha = ReCaptchaV3Field(action='login')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:

            self.fields[field].label = ''
            self.fields[field].help_text = None


    def login(self, *args, **kwargs):

        # Add your own processing here.

        return super(AuthenticationForm, self).login(*args, **kwargs)