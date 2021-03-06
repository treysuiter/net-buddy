from django.db import models
from .netbuddy_users import NetBuddyUser

class SwitchConfiguration(models.Model):

    netbuddy_user = models.ForeignKey(NetBuddyUser, on_delete=models.CASCADE)
    filename= models.CharField(max_length=55)
    config_string = models.TextField(null=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        verbose_name = ("switchconfiguration")
        verbose_name_plural = ("switchconfigurations")

    def __str__(self):
        return self.filename
