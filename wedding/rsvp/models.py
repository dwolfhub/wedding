from django.db import models


class Invitation(models.Model):
    title = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=6)

    def __str__(self):
        return self.title


class Person(models.Model):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    display_name = models.CharField(max_length=50)
    invitation = models.ForeignKey(Invitation, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'people'

    def __str__(self):
        return self.display_name
