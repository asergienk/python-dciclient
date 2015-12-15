# -*- encoding: utf-8 -*-
#
# Copyright 2015 Red Hat, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from dciclient.v1.handlers import dcibaseresource


class JobState(dcibaseresource.DCIBaseResource):
    ENDPOINT_URI = 'jobstates'
    TABLE_HEADERS = ['id', 'status', 'comment', 'job_id', 'team_id', 'etag',
                     'created_at', 'updated_at']

    def __init__(self, dci_client):
        super(JobState, self).__init__(dci_client, self.ENDPOINT_URI)

    def create(self, status, comment, job_id, team_id):
        return super(JobState, self).create(status=status, comment=comment,
                                            job_id=job_id, team_id=team_id)

    def get(self, id, where=None, embed=None):
        return super(JobState, self).get(id=id, where=where, embed=embed)