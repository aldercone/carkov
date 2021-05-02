# carkov #

This is a library for creating and walking simple markov chains. It is
meant for things like text generators (such as ebooks bots and word
generators) and thus is not 'mathetematically correct'. It has some
tools for doing text analysis but more are planned in the future
(stubs exist to illustrate some plans, see TODO.md).

## Command line interface ##

This library includes a command line interface to analyzing text and
then walk the chain and generate text from the analysis.

To analyze a corpus of text files, thus:

`carkov analyze mychain.chain textfile1.txt textfile2.txt ... textfileN.txt`

To walk a chain and generate text form it, thus:

`carkov chain mychain.chain -c 10`

There are two analysis modes currently supported, `english` and
`word`, which are passed to the analyze method with the `-m`
argument. `english` mode analyzes the input in a word-wise method: the
input is segmented into (English-style) sentences, each of which are
analyzed as separate chains of words. `word` segments the input into
tokens, each of which is analyzed as a series of characters
separately.

Analysis also allows a window size to be specified, so that each item
in the chain may be a fixed series of items of a specific length (for
example, the word `foo` with a window of 2, would analyze to (_, _) ->
'f', (_, f) -> o, (f, o) -> o, etc). The wider the window, the more
similar or identical to the input stream the output becomes since
there are fewer total options to follow any given token. This is
specified with the analysis command line with the `-w` argument.

## About Library ##

The library itself exposes objects and interfaces to do the same as
the command line above. A todo item on this project is to generate
documentation and examples, but looking at the contents of __main__.py
should be instructive. The library is written in such a way as to be
pretty agnostic about the items that are chained, and hypothetically
any sequential set of things could work for this. Some framework would
have to be written to support displaying these sorts of things but it
should be possible if non-textual data were desired.

The library also provides a few mechanisms for serializing a ready to
use chain for reuse in other projects. The command line makes use of
the binary serialization mechanism (which uses `msgpack`) to save
chains from the analysis step for re-use in the chain step. There is
also a mechanism which produces a python source file tthat can be
embedded in a target project so that a python project can use the
chain without having to include an extra data file. It should be noted
that this of course is extremely inefficient for large chains.
