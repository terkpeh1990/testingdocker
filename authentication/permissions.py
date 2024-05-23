from rest_framework import permissions


class IsCreateUser(permissions.BasePermission):
    def has_permission(self, request, view):
        # Check if the user's group has permission to create brand
        return request.user.groups.filter(permissions__codename='custom_create_user').exists()

class IsUpdateUser(permissions.BasePermission):
    def has_permission(self, request, view):
        # Check if the user's group has permission to update Brand
        return request.user.groups.filter(permissions__codename='custom_update_user').exists()


class IsViewUser(permissions.BasePermission):
    def has_permission(self, request, view):
        # Check if the user's group has permission to view brand
        return request.user.groups.filter(permissions__codename='custom_view_user').exists()


class IsDeleteUser(permissions.BasePermission):
    def has_permission(self, request, view):
        # Check if the user's group has permission to delete brand
        return request.user.groups.filter(permissions__codename='custom_delete_user').exists()


# class IsCreateUse(permissions.BasePermission):
#     def has_permission(self, request, view):
#         # Check if the user's group has permission to create brand
#         return request.user.groups.filter(permissions__codename='custom_create_user').exists()

# class IsUpdateUser(permissions.BasePermission):
#     def has_permission(self, request, view):
#         # Check if the user's group has permission to update Brand
#         return request.user.groups.filter(permissions__codename='custom_update_user').exists()


# class IsViewUser(permissions.BasePermission):
#     def has_permission(self, request, view):
#         # Check if the user's group has permission to view brand
#         return request.user.groups.filter(permissions__codename='custom_view_user').exists()


# class IsDeleteUser(permissions.BasePermission):
#     def has_permission(self, request, view):
#         # Check if the user's group has permission to delete brand
#         return request.user.groups.filter(permissions__codename='custom_delete_user').exists()    


            