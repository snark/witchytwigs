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
    parser.add_argument(
        '--site',
        help='path to the site directory (default: .)'
    )
    parser.add_argument(
        '--out',
        help='path to write the output to (default: ./out)'
    )

    args = parser.parse_args()

    # For now, we are hardcoding
    cwd = os.getcwd()
    out_dir = args.out or cwd
    site_dir = args.site or os.path.join(cwd, 'out')

    util.generate(site_dir, out_dir)


if __name__ == '__main__':
    main()

