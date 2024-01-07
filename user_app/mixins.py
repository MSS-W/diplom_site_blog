from django.http import HttpResponseForbidden


class PermissionGroupRequiredMixin:
    group_required = None

    def dispatch(self, request, *args, **kwargs):
        if request.user.groups.filter(name=self.group_required).exists():
            return super().dispatch(request, *args, **kwargs)
        else:
            raise HttpResponseForbidden("Вы не имеете доступа к этой странице.")


class PermissionSameAuthorMixin:

    def dispatch(self, request, *args, **kwargs):
        if request.user == self.get_object().author:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise HttpResponseForbidden("Вы не имеете доступа к этой странице.")
