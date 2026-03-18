from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect

class RoleRequiredMixin(AccessMixin):
    """
    Mixin for class-based views that requires a user to have a specific role.
    """
    allowed_roles = []

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
            
        if request.user.role in self.allowed_roles or request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
            
        return redirect('accounts:access_denied')
