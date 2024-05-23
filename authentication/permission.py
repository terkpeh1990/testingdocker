from django.contrib.auth.models import Group, Permission
from .models import User

def user_belongs_to_group_with_permission(user, app_label, codename):
    # Retrieve all groups that the user belongs to
    user_groups = user.groups.all()

    # Check each group for the specified permission
    for group in user_groups:
        if group.permissions.filter(content_type__app_label=app_label, codename=codename).exists():
            return True
    
    return False