################################################################################
# File: typing.py                                                              #
# Project: respondpy                                                           #
# Created Date: 2026-01-07                                                     #
# Author: Matthew Carroll                                                      #
# -----                                                                        #
# Last Modified: 2026-01-07                                                    #
# Modified By: Matthew Carroll                                                 #
# -----                                                                        #
# Copyright (c) 2026 Syndemics Lab at Boston Medical Center                    #
################################################################################
from __future__ import annotations

import sys
import typing

if sys.version_info >= (3, 11):
    from typing import Self
elif typing.TYPE_CHECKING:
    from typing_extensions import Self
else:
    Self = object

__all__ = ["Self"]


def __dir__() -> list[str]:
    return __all__
