# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
#
# Copyright (c) 2024  - NiMiZiS - www.nimizis.com
#                                                hm@nimizis.com
from odoo import  fields, models



class ResCompany(models.Model):
    _inherit = "res.company"

    sales_timbre_account_id = fields.Many2one('account.account', string="Compte comptable timbre Vente",default=lambda self: self.env.ref('l10n_dz.1_pcg_44575'))
    purchase_timbre_account_id = fields.Many2one('account.account', string="Compte comptable timbre Achat",default=lambda self: self.env.ref('l10n_dz.1_pcg_6457'))
    prcent = fields.Float('% timbre',default=1, required=True, tracking=True)
    timbre_min = fields.Integer('Min', default=5, required=True, tracking=True)
    timbre_max = fields.Integer('Max',default=10000, required=True, tracking=True)


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sales_timbre_account_id = fields.Many2one('account.account', string="Compte comptable timbre Vente", related='company_id.sales_timbre_account_id', readonly=False)
    purchase_timbre_account_id = fields.Many2one('account.account', string="Compte comptable timbre Achat", related='company_id.purchase_timbre_account_id', readonly=False)
    prcent = fields.Float('% Timbre',default=1, required=True,related='company_id.prcent', readonly=False)
    timbre_min = fields.Integer('Min', default=5, required=True,related='company_id.timbre_min', readonly=False)
    timbre_max = fields.Integer('Max',default=10000, required=True,related='company_id.timbre_max', readonly=False)
