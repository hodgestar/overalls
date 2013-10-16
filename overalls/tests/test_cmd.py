from unittest import TestCase

from argparse import ArgumentParser

from mock import patch, mock_open

from overalls import __version__
from overalls.core import StaticCollector
from overalls.cmd import OverallsUploader
from overalls.uploaders.coveralls import CoverallsIoUploader

from overalls.tests.utils import mk_coverage_results


class TestOverallsUploader(TestCase):
    def test_create(self):
        u = OverallsUploader()
        self.assertTrue(isinstance(u.parser, ArgumentParser))

    def test_create_parser(self):
        u = OverallsUploader()
        p = u.parser
        self.assertEqual(p.usage, None)
        self.assertEqual(p.version, __version__)
        self.assertEqual(
            p.description, 'Upload coverage results to coveralls.io')

    def test_create_collector_empty(self):
        u = OverallsUploader()
        c = u.create_collector(u.parser.parse_args([]))
        r = c.results()
        self.assertEqual(r.files, [])

    @patch('overalls.cmd.PythonCoverageCollector',
           autospec=True, return_value=object())
    def test_create_collector_py(self, py_mock):
        u = OverallsUploader()
        c = u.create_collector(u.parser.parse_args(['--py']))
        py_mock.assert_called_once_with()
        self.assertEqual(c._collectors, [py_mock.return_value])

    @patch('overalls.cmd.LcovCollector',
           autospec=True, return_value=object())
    @patch('__builtin__.open',
           new_callable=mock_open, create=True)
    def test_create_collector_lcov(self, open_mock, lcov_mock):
        u = OverallsUploader()
        c = u.create_collector(u.parser.parse_args(['--lcov', 'test']))
        lcov_mock.assert_called_once_with(open_mock.return_value)
        open_mock.assert_called_once_with('test')
        self.assertEqual(c._collectors, [lcov_mock.return_value])

    def test_create_uploader(self):
        u = OverallsUploader()
        uploader = u.create_uploader(u.parser.parse_args([]))
        self.assertTrue(isinstance(uploader, CoverallsIoUploader))

    @patch('overalls.cmd.logging.basicConfig')
    def test_run(self, log_mock):
        u = OverallsUploader()
        args = u.parser.parse_args([])
        collector = StaticCollector(mk_coverage_results())
        uploader = CoverallsIoUploader()
        upload_calls = []

        u.parser.parse_args = lambda: args
        u.create_uploader = lambda args: uploader
        u.create_collector = lambda args: collector
        uploader.upload = upload_calls.append
        u.run()

        self.assertEqual(upload_calls, [collector.results()])
        log_mock.assert_not_called()
