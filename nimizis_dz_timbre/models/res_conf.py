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

    fiscal_year = fields.Selection(
        selection=[('2020', 'Loi de finance 2020'),
                   ('2023', 'Loi de finance 2023'),
                   ('2025', 'Loi de finance 2025'),
                   ],string='Loi de finance',default='2025',required=True)



class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sales_timbre_account_id = fields.Many2one('account.account', string="Compte comptable timbre Vente", related='company_id.sales_timbre_account_id', readonly=False)
    purchase_timbre_account_id = fields.Many2one('account.account', string="Compte comptable timbre Achat", related='company_id.purchase_timbre_account_id', readonly=False)

    fiscal_year = fields.Selection(string='Loi de finance',related='company_id.fiscal_year',readonly=False,required=True)

