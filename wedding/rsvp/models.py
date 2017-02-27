import uuid
from django.utils import timezone

from django.db import models


class Invitation(models.Model):
    token = models.UUIDField(primary_key=True, default=uuid.uuid4,
                             editable=False)
    title = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=6)

    ceremony = models.BooleanField(default=False)

    shuttle = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Person(models.Model):
    token = models.UUIDField(primary_key=True, default=uuid.uuid4,
                             editable=False)
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    display_name = models.CharField(max_length=50)
    invitation = models.ForeignKey(Invitation, on_delete=models.CASCADE)
    coming = models.BooleanField(default=False)
    responded = models.BooleanField(default=False)
    responded_datetime = models.DateTimeField(null=True)

    class Meta:
        verbose_name_plural = 'people'

    def __str__(self):
        return self.display_name

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        # if responded is set to True, make sure the responded_datetime is set
        if self.responded and not self.responded_datetime:
            self.responded_datetime = timezone.now()
        super(Person, self).save()
