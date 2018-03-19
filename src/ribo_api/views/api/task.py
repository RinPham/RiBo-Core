from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from ribo_api.models.task import Task
from ribo_api.models.user import User
from ribo_api.serializers.task import TaskSerializer
from ribo_api.services.utils import Utils


class TaskViewSet(ViewSet):
    view_set = 'task'
    serializer_class = TaskSerializer

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
                "content": "goi dien cho bo",
                "user_id": "5aadf857e3d8ee10db5546ba",
                "intent_id": "5aa810bfe3d8ee4f97613dfa",
                "at_time": "2018-09-08T07:00:00Z",
                "done": false
            }
        ]
        """
        try:
            user = self.request.user
            tasks = Task.objects(user_id=user.id)
            serializer = self.serializer_class(tasks, many=True)
            return Response(serializer.data)
        except Exception as e:
            Utils.log_exception(e)
            raise e

    def create(self, request, *args, **kwargs):
        """
        @apiVersion 1.0.0
        @api {POST} /task Create task
        @apiName TaskCreate
        @apiGroup Ribo_api Task
        @apiPermission Authentication

        @apiHeader {string} Authorization format: token <token_string>
        @apiHeaderExample {json} Request Header Example:
        {
            "Authorization": "token QL7RXWUJKDIISITBDLPRUPQZAXD81XYEHZ4HPL5J"
        }

        @apiParam {string} title
        @apiParam {string} content
        @apiParam {datetime} at_time format '2018-09-08T07:00:00Z'

        @apiSuccess {object} task
        @apiSuccessExample {json}
        {
            "id": "5aafd181e3d8ee3175f5ae84",
            "title": "goi dien cho bo",
            "content": "goi dien cho bo",
            "user_id": "5aadf857e3d8ee10db5546ba",
            "intent_id": "5aa810bfe3d8ee4f97613dfa",
            "at_time": "2018-09-08T07:00:00Z",
            "done": false
        }
        """
        try:
            data = request.data.copy()
            data['user_id'] = request.user.id
            data['intent_id'] = "5aa810bfe3d8ee4f97613dfa"
            serializer = self.serializer_class(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        except Exception as e:
            Utils.log_exception(e)
            raise e

    def update(self, request, pk, *args, **kwargs):
        """
        @apiVersion 1.0.0
        @api {PUT} /task/:id_task Edit task
        @apiName TaskEdit
        @apiGroup Ribo_api Task
        @apiPermission Authentication

        @apiHeader {string} Authorization format: token <token_string>
        @apiHeaderExample {json} Request Header Example:
        {
            "Authorization": "token QL7RXWUJKDIISITBDLPRUPQZAXD81XYEHZ4HPL5J"
        }

        @apiParam {string} title
        @apiParam {string} content
        @apiParam {datetime} at_time format '2018-09-08T07:00:00Z'
        @apiParam {boolean} done

        @apiSuccess {object} task
        @apiSuccessExample {json}
        {
            "id": "5aafd181e3d8ee3175f5ae84",
            "title": "goi dien cho bo",
            "content": "goi dien cho bo",
            "user_id": "5aadf857e3d8ee10db5546ba",
            "intent_id": "5aa810bfe3d8ee4f97613dfa",
            "at_time": "2018-09-08T07:00:00Z",
            "done": false
        }
        """
        try:
            data = request.data.copy()
            task = Task.objects(id = pk)[0]
            serializer = self.serializer_class(task, data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        except Exception as e:
            Utils.log_exception(e)
            raise e

    def delete(self, request,pk, *args, **kwargs):
        """
        @apiVersion 1.0.0
        @api {PUT} /task/:id_task Delete task
        @apiName TaskDelete
        @apiGroup Ribo_api Task
        @apiPermission Authentication

        @apiHeader {string} Authorization format: token <token_string>
        @apiHeaderExample {json} Request Header Example:
        {
           "Authorization": "token QL7RXWUJKDIISITBDLPRUPQZAXD81XYEHZ4HPL5J"
        }

        @apiSuccess 200
        """
        try:
            task = Task.objects(id = pk)
            if len(task) == 0:
                return Response("Id is wrong!", status=404)
            task.delete()
            return Response("Success")
        except Exception as e:
            Utils.log_exception(e)
            raise e