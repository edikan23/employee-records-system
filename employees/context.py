from .roles import can_manage, get_role


def roles(request):
    return {"role": get_role(request.user), "can_manage": can_manage(request.user)}
