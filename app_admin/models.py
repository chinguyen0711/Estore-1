from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    porfolio = models.URLField(blank=True, null=True)
    image = models.ImageField(upload_to='users/', default='users/no_avatar.png')

    def __str__(self) -> str:
        return self.user.username