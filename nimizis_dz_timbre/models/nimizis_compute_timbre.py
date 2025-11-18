# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
#
# Copyright (c) 2025  - NiMiZiS - www.nimizis.com
#                                                hm@nimizis.com
import math

def compute_stamp(fiscal_year,total):
    timbre=0
    if fiscal_year == '2020':
        timbre = math.ceil(total / 100)
        if timbre < 5:
            timbre = 5
        elif timbre > 2500:
            timbre = 2500
    elif fiscal_year == '2023':
        timbre = math.ceil(total / 100)
        if timbre < 5:
            timbre = 5
        elif timbre > 10000:
            timbre = 10000
    elif fiscal_year == '2025':
        if total > 300 and total <= 30000:
            timbre = math.ceil(total / 100)
        elif total > 30000 and total <= 100000:
            timbre = math.ceil(math.ceil(total / 100)*1.5)
        elif total > 100000:
            timbre = math.ceil(math.ceil(total / 100)*2)
        if timbre <5 and timbre !=0:
            timbre=5
    return timbre

