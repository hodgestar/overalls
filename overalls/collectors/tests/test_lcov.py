from unittest import TestCase
from StringIO import StringIO
import pkg_resources

from overalls.collectors.lcov import LcovParser, LcovParserError, LcovCollector
from overalls.core import CoverageResults, Collector, FileCoverage


def mk_coverage(filename=None, coverage=None, extend=True):
    if filename is None:
        filename = __file__
    with open(filename) as f:
        source = f.read()
    len_src = len(source.splitlines())
    if coverage is None:
        coverage = [None] * len_src
    if len(coverage) < len_src:
        coverage.extend([None] * (len_src - len(coverage)))
    return FileCoverage(filename, source, coverage)


class TestLcovParser(TestCase):
    def test_create(self):
        p = LcovParser()
        self.assertTrue(isinstance(p.results, CoverageResults))

    def test_set_record(self):
        p = LcovParser()
        p.set_record("foo", [(1, 0), (2, 1)])
        self.assertEqual(p._source_file, "foo")
        self.assertEqual(p._coverage, [(1, 0), (2, 1)])

    def test_clear_record(self):
        p = LcovParser()
        p.set_record("foo", [(1, 0)])
        p.clear_record()
        self.assertEqual(p._source_file, None)
        self.assertEqual(p._coverage, [])

    def test_store_record(self):
        p = LcovParser()
        cov = mk_coverage(coverage=[0, 1])
        p.set_record(cov.filename, [(1, 0), (2, 1)])
        p.store_record()
        self.assertEqual(p.results.files, [cov])

    def test_store_empty_record(self):
        p = LcovParser()
        self.assertRaises(LcovParserError, p.store_record)

    def test_feed(self):
        p = LcovParser()
        p.feed("SF:/tmp/foo")
        self.assertEqual(p._source_file, "/tmp/foo")

    def test_feed_unknown_line(self):
        p = LcovParser()
        p.feed("UNKNOWN:data")  # should succeed silently

    def test_feed_no_colon(self):
        p = LcovParser()
        p.feed("gibberish")  # should succeed silently

    def test_feed_end_of_record(self):
        p = LcovParser()
        cov = mk_coverage(coverage=[0, 3])
        p.set_record(cov.filename, [(1, 0), (2, 3)])
        p.feed("end_of_record")
        self.assertEqual(p.results.files, [cov])

    def test_handle_sf(self):
        p = LcovParser()
        p.handle_sf("/tmp/foo")
        self.assertEqual(p._source_file, "/tmp/foo")

    def test_handle_da(self):
        p = LcovParser()
        p.handle_da("2,4")
        self.assertEqual(p._coverage, [(2, 4)])
        p.handle_da("3,5")
        self.assertEqual(p._coverage, [(2, 4), (3, 5)])


class TestLcovCollector(TestCase):
    def test_create(self):
        f = StringIO()
        c = LcovCollector(f)
        self.assertTrue(isinstance(c, Collector))

    def test_results(self):
        lcov = pkg_resources.resource_filename(__name__, "example.lcov")
        with open(lcov) as f:
            c = LcovCollector(f)
            r = c.results()
        cov1 = mk_coverage("overalls/__init__.py", coverage=[1])
        cov2 = mk_coverage("overalls/core.py", coverage=[1, 3, 5])
        self.assertEqual(r.files, [cov1, cov2])
