from django.apps import AppConfig
from django.db.models.signals import post_migrate

class HomeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'home'

    def ready(self):
        # Connect the signal to the function
        post_migrate.connect(create_default_groups, sender=self)

def create_default_groups(sender, **kwargs):
    from django.contrib.auth.models import Group
    # Create default groups
    Group.objects.get_or_create(name='Admin')
    Group.objects.get_or_create(name='Acadmission')
    Group.objects.get_or_create(name='Students')




