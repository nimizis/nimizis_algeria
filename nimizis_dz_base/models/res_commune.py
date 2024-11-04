# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
#
# Copyright (c) 2024  - NiMiZiS - www.nimizis.com
#                                                hm@nimizis.com

from odoo import fields, models, api

class ResCommune(models.Model):
    _name = 'res.commune'
    _descritpion = 'Commune'
    _order = 'name,id'

    code = fields.Char(string='Code Commune',
                       help=u'Le code de la commune sur deux positions', required=True)
    state_id = fields.Many2one('res.country.state', string='Wilaya', required=True)
    name = fields.Char(string='Commune', required=True, translate=True)

    code = fields.Char(string='Code Commune', required=True)
    daira = fields.Char(string='Daira', required=False,)
    name_arabe = fields.Char(string='Nom arabe', required=False,)
