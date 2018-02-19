"""
Generate a Witchytwigs site.
"""

from . import __VERSION__
from . import util

import sys
import os


def main():
    """
    Run Witchytwigs as a CLI.
    """
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate a Witchytwigs site (version %s)" % __VERSION__
    )
    args = parser.parse_args()

    # For now, we are hardcoding
    site_dir = '/Users/scook/Documents/Personal/Code/witchytwigs/site'
    out_dir = '/Users/scook/Documents/Personal/Code/witchytwigs/out'

    util.generate(site_dir, out_dir)


if __name__ == '__main__':
    main()

