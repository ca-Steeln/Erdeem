
from django.utils.safestring import mark_safe
from django.template import loader
from django.utils.translation import gettext_lazy as _

from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV3

class ReCaptcha(ReCaptchaV3):
    template_name = "apps/recaptcha/widget.html"

    def render(self, name, value, attrs=None, renderer=None):
        context = self.get_context(name, value, attrs)
        template = loader.get_template(self.template_name)
        return mark_safe(template.render(context))


class ReCaptchaV3Field(ReCaptchaField):
    def __init__(self, action=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.widget = ReCaptcha(action=action, attrs={'data-sitekey': self.public_key})
        self.error_messages = {
            'required': _('Error verifying reCAPTCHA, please try again.')
        }
