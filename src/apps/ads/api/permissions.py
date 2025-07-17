from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user


class IsProposalParticipant(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (obj.ad_sender.user == request.user) or (
            obj.ad_receiver.user == request.user
        )
