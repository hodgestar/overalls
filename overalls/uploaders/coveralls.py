# -*- coding: utf-8 -*-

"""Uploader for coveralls.io."""

import json
import StringIO

import requests

from overalls.core import Uploader


class CoverallsIoUploader(Uploader):

    DEFAULT_API_URL = "https://coveralls.io/api/v1/jobs"

    def __init__(self, api_url=None, service_job_id=None, service_name=None):
        if api_url is None:
            api_url = self.DEFAULT_API_URL
        self._api_url = api_url

        if service_job_id is None:
            service_job_id = self.default_job_id()
        self._service_job_id = service_job_id

        if service_name is None:
            service_name = self.default_service_name()
        self._service_name = service_name

    def result_to_json(self, r):
        return {
            "name": r.name,
            "source": r.source,
            "coverage": r.coverage,
        }

    def post_to_api(self, json_file):
        requests.post(self._api_url, files={'json_file': json_file})

    def upload(self, results):
        source_files = [self.result_to_json(r) for r in results]
        json_data = {
            "service_job_id": self._service_job_id,
            "service_name": self._service_name,
            "source_files": source_files,
        }
        json_file = StringIO(json.dumps(json_data))
        self.post_to_api(json_file)
