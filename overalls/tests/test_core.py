from unittest import TestCase

from overalls.core import (
    FileCoverage, CoverageResults, Collector, StaticCollector, CollectorSet,
    Uploader)


def mk_file_coverage(filename="filename", source="sour\nce",
                     coverage=()):
    return FileCoverage(filename, source, coverage)


def mk_coverage_results(results=1):
    c = CoverageResults()
    for i in range(results):
        c.append(mk_file_coverage())
    return c


class TestFileCoverage(TestCase):
    def test_create(self):
        f = FileCoverage("filename", "sour\nce", [])
        self.assertEqual(f.filename, "filename")
        self.assertEqual(f.source, "sour\nce")
        self.assertEqual(f.coverage, [])


class TestCoverageResults(TestCase):
    def test_create(self):
        r = CoverageResults()
        self.assertEqual(r.files, [])

    def test_append(self):
        r = CoverageResults()
        f = mk_file_coverage()
        r.append(f)
        self.assertEqual(r.files, [f])

    def test_extend(self):
        r1 = CoverageResults()
        f1 = mk_file_coverage()
        r1.append(f1)
        r2 = CoverageResults()
        f2 = mk_file_coverage()
        r2.append(f2)
        r1.extend(r2)
        self.assertEqual(r1.files, [f1, f2])
        self.assertEqual(r2.files, [f2])


class TestCollector(TestCase):
    def test_results(self):
        c = Collector()
        self.assertRaises(NotImplementedError, c.results)


class TestStaticCollector(TestCase):
    def test_create(self):
        c = StaticCollector(mk_coverage_results())
        self.assertTrue(isinstance(c, Collector))

    def test_results(self):
        r = CoverageResults()
        c = StaticCollector(r)
        self.assertEqual(c.results(), r)


class TestCollectorSet(TestCase):
    def test_create(self):
        c = CollectorSet([])
        self.assertTrue(isinstance(c, Collector))

    def test_results_empty_set(self):
        c = CollectorSet([])
        r = c.results()
        self.assertEqual(r.files, [])

    def test_results(self):
        c1 = StaticCollector(mk_coverage_results())
        c2 = StaticCollector(mk_coverage_results())
        c = CollectorSet([c1, c2])
        r = c.results()
        self.assertEqual(r.files, c1.results().files + c2.results().files)


class TestUploader(TestCase):
    def test_upload(self):
        u = Uploader()
        r = CoverageResults()
        self.assertRaises(NotImplementedError, u.upload, r)
