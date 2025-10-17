from django.db import models


class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    double_opt_in = models.BooleanField(default=False)
    source = models.CharField(max_length=120, blank=True)
    tags = models.CharField(max_length=240, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
