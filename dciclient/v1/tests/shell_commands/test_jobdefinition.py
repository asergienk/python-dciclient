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

from __future__ import unicode_literals
import json


def test_prettytable_output(runner):
    result = runner.invoke(['test-create', '--name', 'foo'])
    test = json.loads(result.output)['test']
    result = runner.invoke(['jobdefinition-create', '--name', 'foo',
                            '--test_id', test['id']])
    jobdefinition = json.loads(result.output)['jobdefinition']

    result = runner.invoke(['--format', 'table', 'jobdefinition-show', '--id',
                            jobdefinition['id']])

    output = result.output.split('\n')
    # NOTE(spredzy) : The expected output for a table format looks like the
    #                 following :
    #
    # +------------
    # |  id | name
    # +------------
    # | id1 | name1
    # | id2 | name2
    # | id3 | name3
    # +------------
    #
    # The header variable below represents the header data, when more than one
    # space is located between the string and the '|' space number is shrink to
    # one ( this is what ' '.join(string.split()) does
    #
    # The data variable below represents the actual data, when more than one
    # space is located between the string and the '|' space number is shrink to
    # one ( this is what ' '.join(string.split()) does
    header = ' '.join(output[1].split())
    data = ' '.join(output[3].split())

    expected_data = (jobdefinition['id'], jobdefinition['name'],
                     jobdefinition['priority'], jobdefinition['test_id'],
                     jobdefinition['etag'], jobdefinition['created_at'],
                     jobdefinition['updated_at'])

    assert header == ('| id | name | priority | test_id | etag | created_at '
                      '| updated_at |')

    assert data == '| %s | %s | %s | %s | %s | %s | %s |' % expected_data


def test_list(runner):
    result = runner.invoke(['test-create', '--name', 'foo'])
    test = json.loads(result.output)['test']

    runner.invoke(['jobdefinition-create', '--name', 'foo', '--test_id',
                   test['id']])
    runner.invoke(['jobdefinition-create', '--name', 'bar', '--test_id',
                   test['id']])
    result = runner.invoke(['jobdefinition-list'])
    jobdefinitions = json.loads(result.output)['jobdefinitions']

    assert len(jobdefinitions) == 2
    assert jobdefinitions[0]['name'] == 'foo'
    assert jobdefinitions[1]['name'] == 'bar'


def test_create(runner):
    result = runner.invoke(['test-create', '--name', 'foo'])
    test = json.loads(result.output)['test']
    result = runner.invoke(['jobdefinition-create', '--name', 'foo',
                            '--test_id', test['id']])
    jobdefinition = json.loads(result.output)['jobdefinition']
    assert jobdefinition['name'] == 'foo'


def test_delete(runner):
    result = runner.invoke(['test-create', '--name', 'foo'])
    test = json.loads(result.output)['test']

    result = runner.invoke(['jobdefinition-create', '--name', 'foo',
                            '--test_id', test['id']])
    jobdefinition = json.loads(result.output)['jobdefinition']

    result = runner.invoke(['jobdefinition-delete', '--id',
                            jobdefinition['id'], '--etag',
                            jobdefinition['etag']])
    result = json.loads(result.output)

    assert result['message'] == 'Job Definition deleted.'


def test_show(runner):
    result = runner.invoke(['test-create', '--name', 'foo'])
    test = json.loads(result.output)['test']
    result = runner.invoke(['jobdefinition-create', '--name', 'foo',
                            '--test_id', test['id']])
    jobdefinition = json.loads(result.output)['jobdefinition']

    result = runner.invoke(['jobdefinition-show', '--id', jobdefinition['id']])
    jobdefinition = json.loads(result.output)['jobdefinition']

    assert jobdefinition['name'] == 'foo'