# graphql-authz


GraphQL-Authz is a Python3.6+ port of [GraphQL-Authz](https://github.com/node-casbin/graphql-authz), the node.js
implementation for the [Casbin](https://casbin.org/) authorization middleware.

[![PyPi][pypi-image]][https://pypi.python.org/pypi/graphql_authz]

[![Travis][travis-ci-image]][https://travis-ci.com/Checho3388/graphql_authz]

[pypi-image]: https://img.shields.io/pypi/v/graphql_authz.svg
[travis-ci-image]: https://img.shields.io/travis/Checho3388/graphql_authz.svg

This package should use with [GraphQL-core 3](https://github.com/graphql-python/graphql-core), allowing to limit access to each endpoint
using casbin policy.

## Installation

Install the package using pip.

```shell
pip install graphql-authz
```

Get Started
--------
This package should use with graphql and graphql-middleware.
To limit access to each graphql resource you can use a casbin policy. For example,
given this policy for an [RBAC](https://casbin.org/docs/en/rbac) model:

```csv
p, authorized_user, hello, query
```

Validation can be enforced using:

```python3
import casbin
from authz.middleware import enforcer_middleware

from graphql import graphql_sync, GraphQLSchema, GraphQLObjectType, GraphQLField, GraphQLString

schema = GraphQLSchema(
    query=GraphQLObjectType(
        name="RootQueryType",
        fields={
            "hello": GraphQLField(
                GraphQLString,
                resolve=lambda obj, info: "world")
        }))

enforcer = casbin.Enforcer("model_file.conf", "policy_file.csv")
casbin_middleware = enforcer_middleware(enforcer)


query = """{ hello }"""

# Authorized user ("authorized_user") has access to data
response = graphql_sync(schema, query, middleware=[casbin_middleware], context_value={"role": "authorized_user"})
assert response.data == {"hello": "world"}

# Unauthorized users ("unauthorized_user") are rejected
response = graphql_sync(schema, query, middleware=[casbin_middleware], context_value={"role": "unauthorized_user"})
assert response.errors[0].message == "unauthorized_user can not query hello"
```

For more interesting scenarios see `tests` folder.

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
