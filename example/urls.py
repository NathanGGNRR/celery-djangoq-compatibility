from django.urls import path
from example.views import FileList, FileGenerateNewOnes, RecapView

urlpatterns = [
    path("file/", FileList.as_view()),
    path("file/generate/", FileGenerateNewOnes.as_view()),
    path("file/retrieve/", RecapView.as_view()),
]
