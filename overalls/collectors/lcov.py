# -*- coding: utf-8 -*-

"""An lcov collector."""

from overalls.core import Collector, CoverageResults, FileCoverage


class LcovParserError(Exception):
    """Raised if there is an error parsing an lcov file."""


class LcovParser(object):
    """Parser for gcov/lcov tracefile format.__init__

    See http://ltp.sourceforge.net/coverage/lcov/geninfo.1.php.
    """

    END_OF_RECORD = "end_of_record"

    def __init__(self):
        self.results = CoverageResults()
        self.clear_record()

    def set_record(self, source_file=None, coverage=None):
        if source_file is not None:
            self._source_file = source_file
        if coverage is not None:
            self._coverage = coverage

    def clear_record(self):
        self._source_file = None
        self._coverage = []

    def store_record(self):
        try:
            with open(self._source_file) as source_file:
                source = source_file.read()
        except (TypeError, IOError):
            raise LcovParserError("Failed to read source file %r"
                                  % (self._source_file,))
        num_lines = len(source.splitlines())
        cover_dict = dict(self._coverage)
        coverage = [cover_dict.get(i) for i in range(1, num_lines + 1)]
        self.results.append(FileCoverage(
            filename=self._source_file,
            source=source,
            coverage=coverage,
        ))

    def feed(self, line):
        line = line.strip()
        if line == self.END_OF_RECORD:
            self.store_record()
            self.clear_record()
        else:
            line_type, _, rest = line.partition(':')
            handler = getattr(self, "handle_%s" % line_type.lower(),
                              lambda rest: None)
            handler(rest)

    def handle_sf(self, abs_path):
        """Handle a source filename."""
        self._source_file = abs_path

    def handle_da(self, rest):
        """Handle counts for lines that resulted in executable code."""
        # rest = <line number>,<execution count>[,<checksum>]
        line_number, execution_count = rest.split(',')[:2]
        line_number = int(line_number)
        execution_count = int(execution_count)
        self._coverage.append((line_number, execution_count))


class LcovCollector(Collector):

    def __init__(self, lcov_file):
        self._lcov_file = lcov_file

    def results(self):
        parser = LcovParser()
        for line in self._lcov_file:
            parser.feed(line)
        return parser.results
