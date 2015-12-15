# -*- encoding: utf-8 -*-
#
# Copyright 2015 Red Hat, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import click

from dciclient.v1.shell_commands import cli
from dciclient.v1 import utils

from dciclient.v1.handlers import user


@cli.command("user-list", help="List all users.")
@click.pass_obj
def list(context):
    l_user = user.User(context['session'])
    utils.format_output(l_user.list().json(), context['format'],
                        l_user.ENDPOINT_URI, l_user.TABLE_HEADERS)


@cli.command("user-create", help="Create a user.")
@click.option("--name", required=True)
@click.option("--password", required=True)
@click.option("--role", help="'admin' or 'user'")
@click.option("--team_id", required=True)
@click.pass_obj
def create(context, name, password, role, team_id):
    l_user = user.User(context['session'])
    utils.format_output(l_user.create(name=name, password=password,
                                      role=role, team_id=team_id).json(),
                        context['format'], l_user.ENDPOINT_URI[:-1])


@cli.command("user-update", help="Update a user.")
@click.option("--id", required=True)
@click.option("--etag", required=True)
@click.option("--name")
@click.option("--password")
@click.option("--role", help="'admin' or 'user'")
@click.pass_obj
def update(context, id, etag, name, password, role):
    l_user = user.User(context['session'])
    result = l_user.update(id=id, etag=etag, name=name, password=password,
                           role=role)

    if result.status_code == 204:
        utils.format_output({'id': id,
                             'etag': etag,
                             'message': 'User updated.'}, context['format'])
    else:
        utils.format_output(result.json(), context['format'])


@cli.command("user-delete", help="Delete a user.")
@click.option("--id", required=True)
@click.option("--etag", required=True)
@click.pass_obj
def delete(context, id, etag):
    l_user = user.User(context['session'])
    result = l_user.delete(id=id, etag=etag)

    if result.status_code == 204:
        utils.format_output({'id': id,
                             'message': 'User deleted.'}, context['format'])
    else:
        utils.format_output(result.json(), context['format'])


@cli.command("user-show", help="Show a user.")
@click.option("--id", required=True)
@click.pass_obj
def show(context, id):
    l_user = user.User(context['session'])
    utils.format_output(l_user.get(id=id).json(), context['format'],
                        l_user.ENDPOINT_URI[:-1], l_user.TABLE_HEADERS)