# -*- coding: utf-8 -*-

"""Core classes for overalls."""


class FileCoverage(object):
    """Coverage result for a single file.

    :param str filename:
        Name of the filename the results are for.
    :param str source:
        Source code (newline separated).
    :param list coverage:
        List of coverage results. One entry per line.
        Entries may be an integer (number of lines covered) or
        None (not relevant, e.g. for lines that are comments).
    """

    def __init__(self, filename, source, coverage):
        self.filename = filename
        self.source = source
        self.coverage = coverage

    def __repr__(self):
        return "<%s filename=%r source=%r coverage=%r>" % (
            self.__class__.__name__,
            self.filename,
            self.source[:30],
            self.coverage[:30],
        )

    def __eq__(self, other):
        if not isinstance(other, FileCoverage):
            return NotImplemented
        return all((self.filename == other.filename,
                    self.source == other.source,
                    self.coverage == other.coverage))


class CoverageResults(object):
    """Coverage results."""

    def __init__(self):
        self.files = []

    def append(self, file_coverage):
        self.files.append(file_coverage)

    def extend(self, results):
        self.files.extend(results.files)


class Collector(object):
    """Object that knows how collect coverage results from a single source."""

    def results(self):
        """Should read the coverage source and return a `Results` instance."""
        raise NotImplementedError("Collectors should implement .results.")


class StaticCollector(Collector):
    """Collector that returns a static set of results."""

    def __init__(self, results):
        self._results = results

    def results(self):
        return self._results


class CollectorSet(Collector):
    """Collector that combines results from a set of other collectors."""

    def __init__(self, collectors):
        self._collectors = collectors

    def results(self):
        combined = CoverageResults()
        for collector in self._collectors:
            combined.extend(collector.results())
        return combined


class Uploader(object):
    """Object that knows how to upload coverage results somewhere."""

    def upload(self, results):
        """Upload a set of `Results`."""
        raise NotImplementedError("Uploaders should implement .upload.")
