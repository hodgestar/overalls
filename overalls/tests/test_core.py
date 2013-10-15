from unittest import TestCase

from overalls.core import FileCoverage


class TestFileCoverage(TestCase):
    def test_create(self):
        f = FileCoverage("filename", "sour\nce", [])
        self.assertEqual(f.filename, "filename")
        self.assertEqual(f.source, "sour\nce")
        self.assertEqual(f.coverage, [])
