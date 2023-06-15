from django.db import models


class Tecnologia(models.Model):
    nome = models.CharField(max_length=25)

    def __str__(self) -> str:
        return self.nome