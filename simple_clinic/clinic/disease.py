# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: sebanie15
"""
from dataclasses import dataclass


@dataclass
class Diseases:
    """
    klasa choroby
    """
    name: str
    description: str = ''
