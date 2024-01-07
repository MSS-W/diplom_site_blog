from functools import wraps

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404


def set_template(special_template, role_field):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(self, request, *args, **kwargs):
            user = get_object_or_404(User, username=self.kwargs.get('username'))
            if user == self.request.user and user.groups.filter(name=self.extended_group).exists():
                self.template_name = special_template
                setattr(self, role_field, True)
            return view_func(self, request, *args, **kwargs)

        return wrapper

    return decorator
