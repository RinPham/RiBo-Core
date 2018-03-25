import os
import channels.asgi

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ribo_core.settings.production")
channel_layer = channels.asgi.get_channel_layer()