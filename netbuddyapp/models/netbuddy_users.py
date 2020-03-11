from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class NetBuddyUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    current_router_ip = models.CharField(max_length=55, null=True)
    current_vlan_ip = models.CharField(max_length=55, null=True)
    ssh_username = models.CharField(max_length=55)
    ssh_password = models.CharField(max_length=55)
   
# These receiver hooks allow you to continue to
# work with the `User` class in your Python code.

# Every time a `User` is created, a matching `NetBuddyUser`
# object will be created and attached as a one-to-one
# property

@receiver(post_save, sender=User)
def create_netbuddy_user(sender, instance, created, **kwargs):
    if created:
        NetBuddyUser.objects.create(user=instance)

# Every time a `User` is saved, its matching `NetBuddyUser`
# object will be saved.
@receiver(post_save, sender=User)
def save_netbuddy_user(sender, instance, **kwargs):
    instance.netbuddyuser.save()