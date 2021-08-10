
import sys
import os

from .util.run import run_subcommand
from argparse import ArgumentParser
from . import META_COMMANDS

def main():

    parser = ArgumentParser()

    # ========================= #
    # COMMAND ENTRIES           #
    # ========================= #

    parser.add_argument(
        'subcommand'
        ,nargs=1
        ,type=str
        ,help="The command to be executed."
    )

    parser.add_argument(
        'subcommand_args'
        ,nargs="*"
        ,type=str
        ,help="The command arguments to be used by the subcommand."
    )

    # ========================= #
    # OPTIONAL KEYS             #
    # ========================= #

    parser.add_argument(
        '--https'
        ,required=False
        ,action="store_true"
        ,help="Enable HTTPS Mode."
    )

    parser.add_argument(
        '--token'
        ,required=False
        ,type=str
        ,help="Provide token for https."
    )

    parser.add_argument(
        '--upgrade'
        ,required=False
        ,action="store_true"
        ,help="Upgrade option for packages."
    )

    parser.add_argument(
        '--force'
        ,required=False
        ,action="store_true"
        ,help="Force option for packages."
    )

    parser.add_argument(
        '--user'
        ,required=False
        ,action="store_true"
        ,help="Install packages on user pip site repository."
    )

    parser.add_argument(
        '--debug'
        ,required=False
        ,action="store_true"
        ,help="Enable debug mode."
    )

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    
    argv = sys.argv[1:]
    args = parser.parse_args(argv)

    if not run_subcommand(
        subcommand=args.subcommand[0].lower()
        ,subcommand_args=args.subcommand_args
        ,pwd=os.getcwd()
        # KWARGS
        ,https=args.https
        ,token=args.token
        ,upgrade=args.upgrade
        ,force=args.force
        ,user=args.user
        ,debug=args.debug
    ):
        parser.print_help()