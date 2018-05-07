from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from ribo_api.serializers.message import MessageSerializer
from ribo_api.services.conversation import ConversationService
from ribo_api.services.utils import Utils


class MessageViewSet(ViewSet):
    view_set = 'messages'
    serializer_class = MessageSerializer

    def list(self, request, *args, **kwargs):
        """
        @apiVersion 1.0.0
        @api {GET} /messages Get list task
        @apiName TaskList
        @apiGroup Ribo_api Task
        @apiPermission Authentication

        @apiHeader {string} Authorization format: token <token_string>
        @apiHeaderExample {json} Request Header Example:
        {
            "Authorization": "token QL7RXWUJKDIISITBDLPRUPQZAXD81XYEHZ4HPL5J"
        }

        @apiParam {string} user_id
        @apiParam {string} body

        @apiSuccess {object[]} messages
        @apiSuccessExample {json}
        [
            {
                "content" : {
                  "answer_text" : "Go to work",
                  "question_text" : "How should I name this reminder?",
                  "from_who" : 0
                },
                "action" : "reminders.add",
                "updated_at" : "2018-04-12T10:35:11.815000Z",
                "id" : "5acf35f6e3d8ee1172a41ea5",
                "next_question_id" : null,
                "created_at" : "2018-04-12T10:33:26.675000Z",
                "slots" : [

                ],
                "user_id" : "5acf1ee4e3d8ee13b1051b82"
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
