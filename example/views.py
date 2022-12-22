import logging

from enum import Enum
from example.models import File
from example.serializers import FileSerializer, DjangoQSerializer
from rest_framework import generics, mixins, response, status
import uuid
from faker import Faker
import os
from django.core.files.base import ContentFile
from django.conf import settings
from pathlib import Path
from django_q.tasks import async_task
from celery import shared_task
from poccelery.celery import app
from django_q.models import OrmQ

celery_logger = logging.getLogger("celery")

class AsyncRuleEnum(Enum):
    CELERY = 0
    DJANGO_Q = 1
    SYNCHRONE = 2
    CELERY_DJANGO_Q = 3


class FileList(generics.ListCreateAPIView):
    queryset = File.objects.all()
    serializer_class = FileSerializer


class RecapView(generics.RetrieveAPIView):
    def get(self, request):
        i = app.control.inspect()
        queues = OrmQ.objects.all()
        return response.Response(
            {
                "django_q": DjangoQSerializer(queues, many=True).data,
                "django_q_continue": queues.exists(),
                "celery": list(i.reserved().items())[0][1],
                "celery_continue": len(list(i.reserved().items())[0][1]) > 0 or len(list(i.active().items())[0][1]) > 0,
                "celery_active_workers": len(list(i.active().items())[0][1]),
            },
            status=status.HTTP_200_OK,
        )


class FileGenerateNewOnes(
    mixins.CreateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView
):
    queryset = File.objects.all()
    serializer_class = FileSerializer

    def post(self, request, *args, **kwargs):
        async_rule = int(request.data["asyncRule"])
        multiple = int(request.data["multiple"])
        quantity = int(request.data["quantity"])
        if async_rule == AsyncRuleEnum.SYNCHRONE.value:
            if multiple:
                for _ in range(0, quantity):
                    AsyncClass.create_files()
            else:
                AsyncClass.create_files()
            return response.Response(
                self.serializer_class(File.objects.all(), many=True).data,
                status=status.HTTP_201_CREATED,
            )
        elif async_rule == AsyncRuleEnum.DJANGO_Q.value:
            if multiple:
                for _ in range(0, quantity):
                    async_task(AsyncClass.create_files)
            else:
                async_task(AsyncClass.create_files)
            return response.Response(status=status.HTTP_201_CREATED)

        elif async_rule == AsyncRuleEnum.CELERY.value:
            if multiple:
                for _ in range(0, quantity):
                    AsyncClass.async_create_files.apply_async(queue="esms_flow")
            else:
                AsyncClass.async_create_files.apply_async(queue="esms_flow")
            return response.Response(status=status.HTTP_201_CREATED)

        elif async_rule == AsyncRuleEnum.CELERY_DJANGO_Q.value:
            if multiple:
                for _ in range(0, quantity):
                    async_task(AsyncClass.create_files)
                    AsyncClass.async_create_files.apply_async(queue="esms_flow")
            else:
                async_task(AsyncClass.create_files)
                AsyncClass.async_create_files.apply_async(queue="esms_flow")
            return response.Response(status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        files = Path(f"{settings.MEDIA_ROOT}files/").glob("*")
        for file in files:
            os.remove(file)
        File.objects.all().delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)


class AsyncClass(object):
    def create_files():
        faker = Faker()
        for _ in range(10):
            file_name = f"{uuid.uuid4().hex}.txt"
            content = ""
            for _ in range(10000):
                content += f"{faker.text()} \r\n"
            file = File.objects.create(filename=file_name)
            file.file = ContentFile(content, file_name)
            file.save()

    @shared_task
    def async_create_files():
        faker = Faker()
        for _ in range(10):
            file_name = f"{uuid.uuid4().hex}.txt"
            celery_logger.debug(f'Fichier: {file_name}')
            content = ""
            for _ in range(10000):
                content += f"{faker.text()} \r\n"
            file = File.objects.create(filename=file_name)
            file.file = ContentFile(content, file_name)
            file.save()
