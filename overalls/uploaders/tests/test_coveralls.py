from unittest import TestCase
import json

from mock import patch

from overalls.uploaders.coveralls import CoverallsIoUploader
from overalls.tests.utils import mk_file_coverage, mk_coverage_results
from overalls.core import Uploader


class TestCoverallsIoUploader(TestCase):
    def test_create(self):
        c = CoverallsIoUploader()
        self.assertTrue(isinstance(c, Uploader))
        self.assertEqual(c._debug, False)

    def test_create_override_defaults(self):
        c = CoverallsIoUploader(
            api_url="http://foo",
            service_name="name",
            service_job_id="job-id",
            repo_token="token",
            debug=True)
        self.assertEqual(c._debug, True)
        self.assertEqual(c._api_url, "http://foo")
        self.assertEqual(c._service_name, "name")
        self.assertEqual(c._service_job_id, "job-id")
        self.assertEqual(c._repo_token, "token")

    def test_result_to_json(self):
        f = mk_file_coverage(coverage=[1, 0, 2])
        c = CoverallsIoUploader()
        self.assertEqual(c.result_to_json(f), {
            "name": "filename",
            "source": "sour\nce",
            "coverage": [1, 0, 2],
        })

    @patch('overalls.uploaders.coveralls.requests.post')
    def test_post_to_api(self, mock_post):
        c = CoverallsIoUploader()
        json_file = object()
        c.post_to_api(json_file)
        mock_post.called_once_with(
            CoverallsIoUploader.DEFAULT_API_URL,
            files={'json_file': json_file},
        )

    @patch('overalls.uploaders.coveralls.CoverallsIoUploader.post_to_api')
    def test_upload(self, mock_post):
        c = CoverallsIoUploader()
        r = mk_coverage_results()
        c.upload(r)
        mock_post.assert_called_once()
        [json_file], kw = mock_post.call_args
        self.assertEqual(kw, {})
        self.assertEqual(json.loads(json_file.getvalue()), {
            "service_name": CoverallsIoUploader.DEFAULT_SERVICE_NAME,
            "service_job_id": CoverallsIoUploader.DEFAULT_JOB_ID,
            "source_files": [
                {"coverage": [], "name": "filename", "source": "sour\nce"},
            ],
        })
