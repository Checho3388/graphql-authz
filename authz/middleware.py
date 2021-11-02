from authz.exceptions import PermissionInsufficientError
from authz.utils import info_to_path

ANONYMOUS = "*"


def enforcer_middleware(enforcer):
    def graphql_middleware(next, root, info, **args):
        context = info.context or {}

        role = context.get("role", ANONYMOUS)
        path = info_to_path(info)
        action = info.operation.operation.value

        passed = enforcer.enforce(role, path, action)
        if passed:
            return next(root, info, **args)
        else:
            if role == ANONYMOUS:
                role = "anonymous"
            raise PermissionInsufficientError(f"{role} can not {action} {path}")

    return graphql_middleware
