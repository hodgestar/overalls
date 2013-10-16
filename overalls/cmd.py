# -*- coding: utf-8 -*-

from argparse import ArgumentParser

from overalls import __version__
from overalls.core import CollectorSet
from overalls.collectors.python import PythonCoverageCollector
from overalls.collectors.lcov import LcovCollector
from overalls.uploaders.coveralls import CoverallsIoUploader


class OverallsUploader(object):
    def __init__(self):
        self.parser = self.create_parser()

    def create_parser(self):
        parser = ArgumentParser(
            version=__version__,
            description="Upload coverage results to coveralls.io",
        )
        parser.add_argument("--py", action="store_true")
        parser.add_argument("--lcov", action="append")
        return parser

    def create_collector(self, args):
        collectors = []
        if args.py:
            collectors.append(PythonCoverageCollector())
        for lcov_file in (args.lcov or ()):
            collectors.append(LcovCollector(open(lcov_file)))
        return CollectorSet(collectors)

    def create_uploader(self, args):
        return CoverallsIoUploader()

    def run(self):
        args = self.parser.parse_args()
        collector = self.create_collector(args)
        results = collector.results()
        uploader = self.create_uploader(args)
        uploader.upload(results)
