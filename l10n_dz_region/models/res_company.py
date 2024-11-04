# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
#
# Copyright (c) 2024  - NiMiZiS - www.nimizis.com
#                                                hm@nimizis.com


from odoo import fields, models, api,_

class Country(models.Model):
    _inherit = 'res.company'

    nis = fields.Char(related='partner_id.nis',string='N.I.S', readonly=False, track_visibility='onchange')
    ai = fields.Char(related='partner_id.ai',string='Article d\'imposition', readonly=False, track_visibility='onchange')

    forme_juridique_id = fields.Many2one('forme.juridique',related='partner_id.forme_juridique_id', string='Forme juridique', readonly=False, track_visibility='onchange')
    commune_id = fields.Many2one('res.commune',related='partner_id.commune_id', string='Commune',domain="[('state_id', '=?', state_id)]", readonly=False, track_visibility='onchange')
    share_capital = fields.Float('Capital Social', track_visibility='onchange')

    # region_id = fields.Many2one('res.region', string='Region',related='state_id.region_id', store=True, readonly=True)
