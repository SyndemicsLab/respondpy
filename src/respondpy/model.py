################################################################################
# File: model.py                                                               #
# Project: respondpy                                                           #
# Created Date: 2026-06-05                                                     #
# Author: Matthew Carroll                                                      #
# -----                                                                        #
# Last Modified: 2026-07-20                                                    #
# Modified By: Matthew Carroll                                                 #
# -----                                                                        #
# Copyright (c) 2026 Syndemics Lab at Boston Medical Center                    #
################################################################################
from __future__ import annotations

from ._core.model import Model  # pylint: disable=E0611,E0401 # type: ignore[reportMissingModuleSource]

__all__: list[str] = ['Model']
