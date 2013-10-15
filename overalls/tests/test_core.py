from unittest import TestCase

from overalls.core import FileCoverage, CoverageResults


def mk_file_coverage(filename="filename", source="sour\nce",
                     coverage=()):
    return FileCoverage(filename, source, coverage)


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
