from overalls.core import FileCoverage, CoverageResults


def mk_file_coverage(filename="filename", source="sour\nce",
                     coverage=()):
    return FileCoverage(filename, source, coverage)


def mk_coverage_results(results=1):
    c = CoverageResults()
    for i in range(results):
        c.append(mk_file_coverage())
    return c
