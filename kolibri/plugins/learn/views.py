from __future__ import absolute_import, print_function, unicode_literals

from django.conf import settings
from django.views.generic.base import TemplateView
from kolibri.content.content_db_router import using_content_database
from kolibri.content.models import ContentNode, ChannelMetadataCache
from kolibri.content.serializers import ContentNodeSerializer, ChannelMetadataCacheSerializer
from rest_framework.renderers import JSONRenderer


class LearnView(TemplateView):
    template_name = "learn/learn.html"

    def get_context_data(self, **kwargs):
        context = super(LearnView, self).get_context_data(**kwargs)
        context['kolibri'] = settings.KOLIBRI_CORE_JS_NAME
        context['channelList'] = {}
        context['channel_id'] = ''
        context['nodes'] = []
        context['rootnode'] = []

        channels = ChannelMetadataCache.objects.all()
        if not channels:
            return context
        else:
            channel_serializer = ChannelMetadataCacheSerializer(channels, many=True)
            channel_list = JSONRenderer().render(channel_serializer.data)
            context['channelList'] = channel_list

            cookie_current_channel = self.request.COOKIES.get("currentChannel")
            channelExists = False
            for channel in ChannelMetadataCache.objects.all():
                if channel.id == cookie_current_channel:
                    channelExists = True
                    break
            if (cookie_current_channel is not None) and channelExists:
                channel_id = cookie_current_channel
            else:
                channel_id = ChannelMetadataCache.objects.first().id

            context['channel_id'] = channel_id

            with using_content_database(channel_id):
                root_node = ContentNode.objects.get(parent__isnull=True)
                top_level_nodes = root_node.get_children()
                mcontext = {'request': self.request}
                topics_serializer = ContentNodeSerializer(top_level_nodes, context=mcontext, many=True)
                root_node_serializer = ContentNodeSerializer(root_node, context=mcontext)
                context['nodes'] = JSONRenderer().render(topics_serializer.data)
                context['rootnode'] = JSONRenderer().render(root_node_serializer.data)

        return context
