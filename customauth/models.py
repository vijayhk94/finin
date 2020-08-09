from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import BooleanField


# Create your models here.


class JWTToken(models.Model):
    token = models.CharField(max_length=500)
    user = models.ForeignKey(get_user_model(), related_name="token_user", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    is_expired = BooleanField(default=False)

    class Meta:
        unique_together = ("token", "user")
