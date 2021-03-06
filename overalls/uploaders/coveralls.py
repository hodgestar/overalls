# -*- coding: utf-8 -*-

"""Uploader for coveralls.io."""

import os
import json
import StringIO
import logging

import requests

from overalls.core import Uploader


log = logging.getLogger(__name__)


class CoverallsIoUploader(Uploader):

    DEFAULT_API_URL = "https://coveralls.io/api/v1/jobs"
    DEFAULT_SERVICE_NAME = "travis-ci"
    DEFAULT_JOB_ID = os.environ.get('TRAVIS_JOB_ID', '')
    DEFAULT_REPO_TOKEN = os.environ.get('COVERALLS_REPO_TOKEN', None)

    def __init__(self, api_url=None, service_name=None,
                 service_job_id=None, repo_token=None,
                 debug=False):
        self._debug = debug

        if api_url is None:
            api_url = self.DEFAULT_API_URL
        self._api_url = api_url

        if service_name is None:
            service_name = self.DEFAULT_SERVICE_NAME
        self._service_name = service_name

        if service_job_id is None:
            service_job_id = self.DEFAULT_JOB_ID
        self._service_job_id = service_job_id

        if repo_token is None:
            repo_token = self.DEFAULT_REPO_TOKEN
        self._repo_token = repo_token

    def result_to_json(self, r):
        return {
            "name": r.filename,
            "source": r.source,
            "coverage": r.coverage,
        }

    def post_to_api(self, json_file):
        if self._debug:
            log.info("Uploading to %s" % (self._api_url,))
            log.info("Uploading data: %s" % json_file.getvalue())
        response = requests.post(self._api_url, files={'json_file': json_file})
        if self._debug:
            log.info("Coveralls.io reply [%s]: %s"
                     % (response.status_code, response.content))

    def upload(self, results):
        source_files = [self.result_to_json(r) for r in results.files]
        json_data = {
            "service_job_id": self._service_job_id,
            "service_name": self._service_name,
            "source_files": source_files,
        }
        if self._repo_token:
            json_data["repo_token"] = self._repo_token
        json_file = StringIO.StringIO(json.dumps(json_data))
        self.post_to_api(json_file)
