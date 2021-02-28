#
# carkov markov chain library
# © Copyright 2021 by Aldercone Studio <aldercone@gmail.com>
# This is free software, see the included LICENSE for terms and conditions.
#

"""
Various utilities the chainers and analyzers use.
"""

from bisect import bisect


def merge_dict(into, outof, mergefunction = lambda x, y: x + y):
    """
    Given two dictionries of dictionaries, merge them together by applying the mergefunction to the
    values of the second level dictionary.

    Arguments:
        into: The dictionary that is being operated on which gets modified.
        outof: The dictionary to merge into into.
        mergefunction: A function applied to every value in the second level dictionries, defaults to
                       adding the two values together.

    Returns:
        into dictionary after modification.
    """
    for key in outof.keys():
        if key in into:
            for innerkey in outof[key].keys():
                if innerkey in into[key]:
                    into[key][innerkey] = mergefunction(into[key][innerkey], outof[key][innerkey])
                else:
                    into[key][innerkey] = outof[key][innerkey]
        else:
            into[key] = outof[key]
    return into


def convert_counts(ind):
    """
    Convert counts produced by analyzers into the statistics counts used by chainers.

    Arguments:
        ind (dict): The second level dictionary of a counts dictionary

    Returns:
        dict: A copy of ind with the values updated for chainer use.
    """
    out = {}
    for k in ind:
        out[k] = [ind[k], 0]

    return out


def merge_stats(into, outof):
    """
    Perform a merge_dict in a way safe for the statistics dictionaries used by chainers.

    Arguments:
        into: The dictionary to modify
        outof: The dictionary to merge into into.

    Returns:
        into (after modification)

    """
    def stats_merge_function(i, o):
        out = [0, 0]
        out[0] = i[0] + o[0]
        out[1] = 0
        return out
    return merge_dict(into, outof, stats_merge_function)


def weighted_choice(random_state, values, weights):
    """
    Choose a random value in a weighted manner.

    Arguments:
        random_state: A random.Random instance
        values: A list of values to choose from
        weights: The weights that corrospond to each value

    Returns:
        The selected value
    """
    total = 0
    cum_weights = []
    for w in weights:
        total += w
        cum_weights.append(total)
    x = random_state.random() * total
    i = bisect(cum_weights, x)
    return values[i]


def weighted_stat_choice(random_state, stats):
    """
    Perform a weighted choice on a stat dictionary as used in chainers.

    Arguments:
        random_state: A random.Random instance
        stats: A stats dictionary from a chainer
    """
    values = tuple(stats.keys())
    weights = tuple(stats[x][1] for x in values)
    return weighted_choice(random_state, values, weights)
