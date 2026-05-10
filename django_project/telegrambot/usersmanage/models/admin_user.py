from django.contrib.auth.models import AbstractUser

class AdminUser(AbstractUser):
    USERNAME_FIELD = "username"

    def __str__(self):
        return f"{self.username}"