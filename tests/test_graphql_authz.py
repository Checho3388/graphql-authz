#!/usr/bin/env python

"""Tests for `graphql_authz` package."""
import os

import casbin
from graphql import (
    GraphQLArgument,
    GraphQLField,
    GraphQLInt,
    GraphQLList,
    GraphQLObjectType,
    GraphQLSchema,
    GraphQLString,
    graphql_sync,
)

from authz.middleware import enforcer_middleware


TESTS_PATH = os.path.dirname(__file__)


def given_a_graphql_schema() -> GraphQLSchema:
    ticket_type = GraphQLObjectType(
        name="TicketType", fields={
            "id": GraphQLField(GraphQLInt),
            "message": GraphQLField(GraphQLString),
        }
    )
    member_type = GraphQLObjectType(
        name="MemberType", fields={
            "id": GraphQLField(GraphQLInt),
            "name": GraphQLField(GraphQLString),
            "tickets": GraphQLField(
                GraphQLList(ticket_type),
                resolve=lambda member, _info: [
                    {"id": 1, "message": f"Member {member['id']}, Ticket: 1"},
                    {"id": 2, "message": f"Member {member['id']}, Ticket: 2"},
                    {"id": 3, "message": f"Member {member['id']}, Ticket: 3"},
                    {"id": 4, "message": f"Member {member['id']}, Ticket: 4"},
                ]
            ),
        }
    )
    project_type = GraphQLObjectType(
        name="ProjectType", fields={
            "id": GraphQLField(GraphQLInt),
            "name": GraphQLField(GraphQLString),
            "members": GraphQLField(
                GraphQLList(member_type),
                resolve=lambda project, _info: [
                    {"id": 1, "name": f"Project {project['id']}, Member: 1"},
                    {"id": 2, "name": f"Project {project['id']}, Member: 2"},
                ]
            ),
        }
    )
    query_type = GraphQLObjectType(
        name="Query", fields={
            "project": GraphQLField(
                project_type,
                args={
                    "id": GraphQLArgument(
                        GraphQLInt
                    )
                },
                resolve=lambda _source, _info, id:
                {"id": id, "name": f"Project {id}"}
            ),
            "projects": GraphQLField(
                GraphQLList(project_type),
                resolve=lambda _source, _info, id: [
                    {"id": 1, "name": "Project 1"},
                    {"id": 2, "name": "Project 2"},
                ]
            ),
        }
    )
    return GraphQLSchema(query_type)


def given_an_enforcer():
    return casbin.Enforcer(
        os.path.join(TESTS_PATH, "casbin_files/graphql.conf"),
        os.path.join(TESTS_PATH, "casbin_files/graphql_policy.csv")
    )


def test_graphql_middleware():
    schema = given_a_graphql_schema()
    enforcer = given_an_enforcer()

    query = """{
        project(id: 2) {
            id name members {
                id name tickets {
                    id message
                }
            }
        }
    }"""
    casbin_middleware = enforcer_middleware(enforcer)

    response = graphql_sync(schema, query, middleware=[casbin_middleware], context_value={"role": "user"})

    assert response.errors[0].formatted == {
        "message": "user can not query project.name",
        "path": ['project', 'name'],
        "locations": [{'line': 3, 'column': 16}]
    }
    assert response.errors[1].formatted == {
        "message": "user can not query project.members.tickets.message",
        "path": ['project', 'members', 0, 'tickets', 0, 'message'],
        "locations": [{'line': 5, 'column': 24}]
    }
    assert response.errors[2].formatted == {
        "message": "user can not query project.members.tickets.message",
        "path": ['project', 'members', 0, 'tickets', 1, 'message'],
        "locations": [{'line': 5, 'column': 24}]
    }
    assert response.errors[3].formatted == {
        "message": "user can not query project.members.tickets.message",
        "path": ['project', 'members', 0, 'tickets', 2, 'message'],
        "locations": [{'line': 5, 'column': 24}]
    }
    assert response.errors[4].formatted == {
        "message": "user can not query project.members.tickets.message",
        "path": ['project', 'members', 0, 'tickets', 3, 'message'],
        "locations": [{'line': 5, 'column': 24}]
    }
    assert response.errors[5].formatted == {
        "message": "user can not query project.members.tickets.message",
        "path": ['project', 'members', 1, 'tickets', 0, 'message'],
        "locations": [{'line': 5, 'column': 24}]
    }
    assert response.errors[6].formatted == {
        "message": "user can not query project.members.tickets.message",
        "path": ['project', 'members', 1, 'tickets', 1, 'message'],
        "locations": [{'line': 5, 'column': 24}]
    }
    assert response.errors[7].formatted == {
        "message": "user can not query project.members.tickets.message",
        "path": ['project', 'members', 1, 'tickets', 2, 'message'],
        "locations": [{'line': 5, 'column': 24}]
    }
    assert response.errors[8].formatted == {
        "message": "user can not query project.members.tickets.message",
        "path": ['project', 'members', 1, 'tickets', 3, 'message'],
        "locations": [{'line': 5, 'column': 24}]
    }
    assert response.data == {
        'project': {
            'id': 2,
            'name': None,
            'members': [{
                'id': 1, 'name': 'Project 2, Member: 1',
                'tickets': [{'id': 1, 'message': None}, {'id': 2, 'message': None},
                            {'id': 3, 'message': None}, {'id': 4, 'message': None}]
            }, {
                'id': 2, 'name': 'Project 2, Member: 2',
                'tickets': [{'id': 1, 'message': None}, {'id': 2, 'message': None},
                            {'id': 3, 'message': None}, {'id': 4, 'message': None}]
            }]
        }
    }


def test_graphql_middleware_anonymous():
    schema = given_a_graphql_schema()
    enforcer = given_an_enforcer()

    query = """{
        project(id: 2) {
            id name
        }
    }"""
    casbin_middleware = enforcer_middleware(enforcer)

    response = graphql_sync(schema, query, middleware=[casbin_middleware], context_value={"role": "*"})

    assert response.errors[0].formatted == {
        "message": "anonymous can not query project.name",
        "path": ['project', 'name'],
        "locations": [{'line': 3, 'column': 16}]
    }
    assert response.data == {'project': {'id': 2, 'name': None}}

