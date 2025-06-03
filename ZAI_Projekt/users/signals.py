from django.db.models.signals import post_save, post_migrate
from django.contrib.auth.models import User, Group
from django.dispatch import receiver


@receiver(post_migrate)
def create_default_groups(sender, **kwargs):
    for name in ['user', 'moderator', 'admin']:
        Group.objects.get_or_create(name=name)

@receiver(post_save, sender=User)
def assign_user_group(sender, instance, created, **kwargs):
    if created:
        default_group, _ = Group.objects.get_or_create(name='user')
        instance.groups.add(default_group)
