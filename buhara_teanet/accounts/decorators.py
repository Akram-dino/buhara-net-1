from django.contrib.auth.decorators import user_passes_test


def role_required(allowed_roles=None):
    if allowed_roles is None:
        allowed_roles = []

    def check_role(user):
        return user.is_authenticated and user.role in allowed_roles

    return user_passes_test(check_role)