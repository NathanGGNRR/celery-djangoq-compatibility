from django.db import models


class File(models.Model):
    filename = models.CharField(verbose_name="Nom du fichier", max_length=150)
    file = models.FileField(upload_to="files", max_length=200, null=True)

    def __str__(self):
        return self.filename
