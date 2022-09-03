from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.urls import path, re_path

from chat_app.consumers import ChatConsumer
from video.consumers import VideoConsumer
from notification_system.consumers import NotificationConsumer

from django.core.asgi import get_asgi_application




application = ProtocolTypeRouter({
	'http': get_asgi_application(),
	'websocket': AllowedHostsOriginValidator(
		AuthMiddlewareStack(
			URLRouter([
					path('', NotificationConsumer.as_asgi()),
					path('chat/<room_id>/', ChatConsumer.as_asgi()),
					re_path(r'call', VideoConsumer.as_asgi()),
			])
		)
	),
})