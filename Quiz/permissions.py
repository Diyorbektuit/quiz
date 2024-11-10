from rest_framework import permissions

class IsTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.role == "teacher"

class IsTeacherOrSuperuser(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.role != "user"

class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.role == "user"

class IsTestOwnerOrSuperuser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.teacher == request.user or request.user.role == "superuser"

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user






