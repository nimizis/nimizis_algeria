# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
#
# Copyright (c) 2024  - NiMiZiS - www.nimizis.com
#                                                hm@nimizis.com

from . import models

from odoo.api import Environment, SUPERUSER_ID

def post_install(cr, registry):
    env = Environment(cr, SUPERUSER_ID, {'active_test': False})
    env['ir.module.module']._load_module_terms(['nimizis_dz_base'], ['fr_FR'], overwrite=True)