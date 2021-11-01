from graphql import GraphQLResolveInfo

CASBIN_CONTEXT_PATH_CACHE_KEY = '_casbinPathCache'
CASBIN_CONTEXT_ENFORCER_KEY = '_casbinEnforcer'
CASBIN_CONTEXT_ROLE_KEY = '_casbinRole'
CASBIN_AUTH_TYPE_NAME = 'CasbinCanVisit'


def info_to_path(info: GraphQLResolveInfo) -> str:
    """"Get the full path of current endpoint by GraphQLResolveInfo."""
    node = info.path
    full_path = node.key
    while node.prev:
        node = node.prev
        if not isinstance(node.key, int):
            full_path = f"{node.key}.{full_path}"
    return full_path
