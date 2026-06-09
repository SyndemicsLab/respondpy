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
    """Converts a comma-separated string into a list of integers

    Args:
        config_string (str): A comma-separated string

    Returns:
        list[int]: The list of integers from the string
    """
    return [int(x.strip()) for x in config_string.split(delimiter)]
