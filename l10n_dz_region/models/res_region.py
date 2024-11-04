# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
#
# Copyright (c) 2024  - NiMiZiS - www.nimizis.com
#                                                hm@nimizis.com
from odoo import fields, models, api

class ResRegion(models.Model):
    _name = 'res.region'
    _descritpion = 'Region'

    code = fields.Char(string='Code Region',help='Le code de la Region', required=True)
    name = fields.Char(string='La region', required=True, translate=True)




