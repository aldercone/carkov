#
# carkov markov chain library
# © Copyright 2021 by Aldercone Studio <aldercone@gmail.com>
# This is free software, see the included LICENSE for terms and conditions.
#
# This module provides a command line interface to doing some common operations.
#

import argparse
import enum
import pathlib
import sys
import traceback
from random import Random
from typing import cast

from .analyze.abstract import AbstractAnalyzer
from .analyze.english import English
from .analyze.words import Words
from .chain import Chain, from_analyzer
from .serializer import dump_chainer, load_chainer
from .utils import make_sent, make_word

ERROR_NO_FILE = 1
ERROR_EXISTING_OUTPUT = 2
ERROR_WRONG_ORDER = 3
ERROR_WRONG_CLASS = 4


class AnalyzeMode(enum.Enum):
    english = "english"
    word = "word"

    def __str__(self) -> str:
        return self.value


JOINERS = {"Words": make_word, "English": make_sent}


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="python -mcarkov",
                                     description=("Process a text corpus in a markov chain fashion and/or output from"
                                                  "an analysis."))
    subparsers = parser.add_subparsers(dest='command')
    analyze_sub = subparsers.add_parser('analyze', help="Analyze a corpus")
    analyze_sub.add_argument('output', help="Output chain to specified destination", type=pathlib.Path)
    analyze_sub.add_argument('input', help="The corpus to analyze", type=pathlib.Path, nargs='+')
    overappend = analyze_sub.add_mutually_exclusive_group()
    overappend.add_argument('-o', '--overwrite', help='Overwrite output file.', action='store_true')
    overappend.add_argument('-a', '--append', help='Append output file.', action='store_true')
    analyze_sub.add_argument('-w', '--window', help='Select length of analysis window', type=int, default=2)
    analyze_sub.add_argument('-m',
                             '--mode',
                             help='Select analyzis mode',
                             type=AnalyzeMode,
                             choices=list(AnalyzeMode),
                             default=AnalyzeMode.english)

    analyze_sub.add_argument('-t', '--test', help="Output a sample from the chainer generated", action='store_true')

    chain_sub = subparsers.add_parser('chain', help="Output from a chainer")
    chain_sub.add_argument('input', help="The chain file to load", type=pathlib.Path)
    chain_sub.add_argument('-c', '--count', help="Number of chain outputs to output", type=int)

    return parser.parse_args()


def print_chainer_output(chainer: Chain, random_state: Random):
    if chainer.analyzer_class in JOINERS:
        print(JOINERS[cast(str, chainer.analyzer_class)](chainer.walk(random_state, True)))
    else:
        print(chainer.walk(random_state, True))


def command_analyze(args: argparse.Namespace) -> int:
    if not any(x.exists() for x in args.input):
        print("Must specify an existing file as input for the analyzer.")
        return ERROR_NO_FILE

    if args.output.exists() and not (args.overwrite or args.append):
        print("Output file exists, pass --overwrite to overwrite or --append to add to exsiting analysis.")
        return ERROR_EXISTING_OUTPUT

    analyzer: AbstractAnalyzer
    if args.mode == AnalyzeMode.english:
        analyzer = English(args.window)
        # we just dump a whole file into the english analyzer
        for inp in args.input:
            if not inp.exists():
                print(f"warning {inp} does not exist")
                continue
            print(f"analyze: {inp}")
            analyzer.analyze(inp.read_text('utf-8'))
    else:
        analyzer = Words(args.window)
        # we do line-by-line single word dumps into the word analyzer
        for inp in args.input:
            if not inp.exists():
                print(f"warning {inp} does not exist")
                continue
            print(f"analyze: {inp}")
            with inp.open('r') as words:
                for line in words:
                    analyzer.analyze(line.strip().lower())

    if args.append:
        # in append mode we load an existing chain file, and then run the analyzer and merge the contents.
        with open(args.output, 'rb') as old:
            chainer = load_chainer(old)
        if chainer.order != analyzer.order:
            print("Append chainer order isn't the same as the analyzer order.")
            return ERROR_WRONG_ORDER
        if chainer.analyzer_class != analyzer.__class__.__name__:
            print("Append chainer class isn't the same as analyzer class.")
            return ERROR_WRONG_CLASS
        chainer.integrate(analyzer.chain_counts)
    else:
        chainer = from_analyzer(analyzer)

    with open(args.output, 'wb') as output:
        dump_chainer(chainer, output)
    print(f"Wrote chainer to {args.output}")

    if args.test:
        r = Random()
        for _ in range(0, 5):
            print_chainer_output(chainer, r)

    return 0


def command_chain(args: argparse.Namespace) -> int:
    r = Random()

    if not args.input.exists():
        print("Must specify a chain file to load.")
        return ERROR_NO_FILE

    with args.input.open('rb') as inp:
        chainer = load_chainer(inp)

    if args.count < 1:
        args.count = 1

    for _ in range(0, args.count):
        print_chainer_output(chainer, r)

    return 0


def main() -> int:
    args = parse_arguments()
    if args.command == 'analyze':
        return command_analyze(args)
    elif args.command == 'chain':
        return command_chain(args)
    else:
        print("Expect a command `analyze` or `chain`. See --help for details.")
        return 1

    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        print("Unexpected exception!")
        traceback.print_exc()
