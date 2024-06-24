
from django.utils.deprecation import MiddlewareMixin
from django.contrib.messages import get_messages
from json import dumps, loads

class AlertMessagesMiddleware(MiddlewareMixin):

    def process_response(self, request, response):

        if 'HX-Request' in request.headers:
            hx_trigger = response.headers.get('HX-Trigger', {})

            hx_trigger['messages'] = [
                {
                    "message": message.message,
                    "tags": message.tags,
                }
                for message in get_messages(request)
            ]

            response.headers['HX-Trigger'] = dumps(hx_trigger)
        return response
