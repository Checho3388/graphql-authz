from authz.exceptions import PermissionInsufficientError
from authz.utils import (
    CASBIN_CONTEXT_ROLE_KEY,
    info_to_path,
)


def enforcer_middleware(enforcer):
    def graphql_middleware(next, root, info, **args):
        context = info.context or {}

        role = context.get("role", "*")
        path = info_to_path(info)
        action = info.operation.operation.value

        if CASBIN_CONTEXT_ROLE_KEY not in context:
            context[CASBIN_CONTEXT_ROLE_KEY] = role

        passed = enforcer.enforce(role, path, action)
        if passed:
            return next(root, info, **args)
        else:
            if role == "*":
                role = "anonymous"
            raise PermissionInsufficientError(f"{role} can not {action} {path}")

    return graphql_middleware
