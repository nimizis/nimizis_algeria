# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
#
# Copyright (c) 2024  - NiMiZiS - www.nimizis.com
#                                                hm@nimizis.com

from odoo import fields, models, api


class ResCountryState(models.Model):
    _inherit = 'res.country.state'

    commune_ids = fields.One2many('res.commune', 'state_id', string='Communes')
    region_id = fields.Many2one('res.region', string='Region')
    name_arabe = fields.Char(string='Nom arabe', required=False,)

