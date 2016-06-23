import logging
import gzip
import yaml
from scipy.stats import ttest_ind as double_sided_ttest


class TTestCalculator(object):
    def __init__(self, measures):
        self.measures = measures

    def read_one(self, filename):
        """Read the last value of the data of the measures of one file"""
        with gzip.open(filename) as f:
            logging.info("Reading {}".format(filename))
            data = yaml.load(f)
        ans = {}
        for measure in self.measures:
            if measure not in data:
                logging.warn(
                    "Measure {} not in {}. Possibilities: {}".format(
                        measure, filename, data.keys()
                    )
                )
            else:
                ans[measure] = data[measure][-1]
        logging.debug(ans)
        return ans

    def calc(self, first_files, second_files):
        # {measure: ([first1, first2,  ...], [second1, second2, ...])}
        values = {measure: ([], []) for measure in self.measures}
        for i, files in [(0, first_files), (1, second_files)]:
            for f in files:
                for measure, value in self.read_one(f).items():
                    values[measure][i].append(value)
        return {
            measure: double_sided_ttest(*ress, equal_var=False)
            for measure, ress in values.items()
        }


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(
        description="Calculate a two sided Welch's t-test",
        fromfile_prefix_chars='@'
    )
    parser.add_argument("-m", "--measures", nargs="+", required=True,
                        help="Measures to use for t-test (legal options are"
                        " shown when an illegal measure is used)")
    parser.add_argument("-f", "--first", nargs="+", required=True,
                        help="A number of file names to read data from")
    parser.add_argument("-s", "--second", nargs="+", required=True,
                        help="A number of file names to read data from")
    parser.add_argument("-l", "--level", default="INFO", help="Logging level")

    # Parse args and set log level
    args = parser.parse_args()
    logging.basicConfig(level=args.level.upper())

    logging.debug(args)

    values = TTestCalculator(args.measures).calc(
        args.first, args.second
    )

    for measure, ress in values.items():
        print "Measure:", measure
        print "t-statistic:", ress[0]
        print "two-tailed p-value:", ress[1]
