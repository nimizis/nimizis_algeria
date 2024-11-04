# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
#
# Copyright (c) 2024  - NiMiZiS - www.nimizis.com
#                                                hm@nimizis.com

from odoo import fields, models, api

class FormeJuridique(models.Model):
    _name = 'forme.juridique'
    _descritpion = 'Formes juridiques'
    _order = 'id'

    name = fields.Char(string='Acronyme', required=True, translate=True)
    full_name = fields.Char(string='Nom', required=True, translate=True)
    description = fields.Text(string='Description', required=True, translate=True)

