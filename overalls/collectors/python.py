# -*- coding: utf-8 -*-

"""A Python coverage module collector."""

import os.path

from overalls.core import Collector, CoverageResults, FileCoverage

try:
    from coverage.report import Reporter
    from coverage.control import coverage
    HAS_COVERAGE = True
except ImportError as err:
    HAS_COVERAGE = False
    COVERAGE_IMPORT_ERROR = err


class PythonCoverageCollector(Collector):
    def __init__(self, base_dir='.', data_file='.coverage',
                 config_file='.coveragerc'):
        if not HAS_COVERAGE:
            raise COVERAGE_IMPORT_ERROR
        self._base_dir = base_dir
        self._data_file = data_file
        self._config_file = config_file

    def coverage_for_code_unit(self, cu, analysis):
        rel_filename = os.path.relpath(cu.filename, self._base_dir)
        with open(cu.filename) as f:
            source = f.readlines()

        coverage_lines = [None] * len(source)
        missing_lines = set(analysis.missing)
        executable_lines = set(analysis.statements)

        for lineno, line in enumerate(source):
            offset_lineno = lineno + 1
            if offset_lineno in executable_lines:
                if offset_lineno in missing_lines:
                    coverage_lines[lineno] = 0
                else:
                    coverage_lines[lineno] = 1
        return FileCoverage(
            filename=rel_filename, source=''.join(source),
            coverage=coverage_lines)

    def results_for_reporter(self, reporter):
        results = CoverageResults()
        files = [cu.filename for cu in reporter.code_units]

        def cb(cu, analysis):
            results.append(self.coverage_for_code_unit(cu, analysis))

        reporter.report_files(cb, files)
        return results

    def results(self):
        cov = coverage(
            data_file=self._data_file, config_file=self._config_file)
        cov.load()
        reporter = Reporter(cov, cov.config)
        reporter.find_code_units(None)
        return self.results_for_reporter(reporter)
