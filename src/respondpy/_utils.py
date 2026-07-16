################################################################################
# File: _utils.py                                                              #
# Project: respondpy                                                           #
# Created Date: 2026-06-05                                                     #
# Author: Matthew Carroll                                                      #
# -----                                                                        #
# Last Modified: 2026-06-05                                                    #
# Modified By: Matthew Carroll                                                 #
# -----                                                                        #
# Copyright (c) 2026 Syndemics Lab at Boston Medical Center                    #
################################################################################
from __future__ import annotations


def str_to_int_list(config_string: str, *, delimiter: str = ',') -> list[int]:
    """Parse a delimited integer string into a list of integers.

    Whitespace around each token is stripped before conversion.

    Parameters
    ----------
    config_string : str
        Delimited string of integer-like values.
    delimiter : str, default=","
        Token delimiter used to split ``config_string``.

    Returns
    -------
    list of int
        Parsed integers in input order.

    Raises
    ------
    ValueError
        If any token cannot be converted to ``int``.
    """
    return [int(x.strip()) for x in config_string.split(delimiter)]
