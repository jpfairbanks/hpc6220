import argparse

def get_args():
    """A common arguments interface for 
    several programs to share.
    :returns: an argument dictionary

    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--scale',
            default=10, type=int,
            help="use 2**scale data points")
    parser.add_argument('-p', '--procs',
            default=4, type=int,
            help="number of processes to use")
    parser.add_argument('-t', '--tree',
            action='store_true',
            help="use the divide and conquor tree approach")
    parser.add_argument('-v', '--verbose',
            action='store_true',
            help="verbose mode print more stuff")
    return parser.parse_args()
