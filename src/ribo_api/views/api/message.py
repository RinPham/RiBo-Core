from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from ribo_api.serializers.message import MessageSerializer
from ribo_api.services.conversation import ConversationService
from ribo_api.services.utils import Utils


class MessageViewSet(ViewSet):
    view_set = 'task'
    serializer_class = MessageSerializer

    def list(self, request, *args, **kwargs):
        """
        @apiVersion 1.0.0
        @api {GET} /task Get list task
        @apiName TaskList
        @apiGroup Ribo_api Task
        @apiPermission Authentication

        @apiHeader {string} Authorization format: token <token_string>
        @apiHeaderExample {json} Request Header Example:
        {
            "Authorization": "token QL7RXWUJKDIISITBDLPRUPQZAXD81XYEHZ4HPL5J"
        }

        @apiSuccess {object[]} task
        @apiSuccessExample {json}
        [
            {
                "id": "5aafd181e3d8ee3175f5ae84",
                "title": "goi dien cho bo",
                "user_id": "5aadf857e3d8ee10db5546ba",
                "at_time": "2018-09-08T07:00:00Z",
                "done": false,
                "repeat": 0
            }
        ]
        """
        try:
            user = self.request.user
            messages = ConversationService.load_messages(user.id)
            return Response(messages)
        except Exception as e:
            Utils.log_exception(e)
            raise e
