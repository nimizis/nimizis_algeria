# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
#
# Copyright (c) 2024  - NiMiZiS - www.nimizis.com
#                                                hm@nimizis.com
from odoo import models, fields, api
from odoo.tools.misc import format_date, formatLang
from . import nimizis_compute_timbre


class TimbrePurchases(models.Model):
    _inherit = "purchase.order"

    amount_timbre=fields.Monetary(string='Montant du Timbre', readonly=True, compute='_amount_all',tracking=True, store=True)
    if_timbre=fields.Boolean(string='Timbre ?',readonly=True, default=False)
    txt_timbre = fields.Char(string='Loi de finance appliqué', readonly=True,store=1,tracking=True)

    # the function that applies the stamp on the invoice
    def add_timbre(self):
        self.if_timbre = True
        self.txt_timbre = self.company_id.fiscal_year

    # the function that removes the stamp application from the invoice
    def del_timbre(self):
        self.if_timbre = False
        self.txt_timbre = ""

    @api.depends('order_line.price_total', 'if_timbre')
    def _amount_all(self):
        for order in self:
            order_lines = order.order_line.filtered(lambda x: not x.display_type)
            if order.company_id.tax_calculation_rounding_method == 'round_globally':
                tax_results = self.env['account.tax']._compute_taxes([line._convert_to_tax_base_line_dict() for line in order_lines])
                totals = tax_results['totals']
                amount_untaxed = totals.get(order.currency_id, {}).get('amount_untaxed', 0.0)
                amount_tax = totals.get(order.currency_id, {}).get('amount_tax', 0.0)
            else:
                amount_untaxed = sum(order_lines.mapped('price_subtotal'))
                amount_tax = sum(order_lines.mapped('price_tax'))
            amount_timbre=0
            if order.if_timbre:
                amount_timbre = nimizis_compute_timbre.compute_stamp(order.company_id.fiscal_year,amount_untaxed+amount_tax)
            order.amount_timbre = amount_timbre
            order.amount_untaxed = amount_untaxed
            order.amount_tax = amount_tax
            order.amount_total = order.amount_untaxed + order.amount_tax + order.amount_timbre




    @api.depends_context('lang')
    @api.depends('order_line.taxes_id', 'order_line.price_subtotal', 'if_timbre', 'amount_total', 'amount_untaxed')
    def _compute_tax_totals(self):
        for order in self:
            order_lines = order.order_line.filtered(lambda x: not x.display_type)
            tax_totals = self.env['account.tax']._prepare_tax_totals(
                [x._convert_to_tax_base_line_dict() for x in order_lines],
                order.currency_id or order.company_id.currency_id)
            tax_totals['amount_total']=order.amount_total
            tax_totals['formatted_amount_total'] = formatLang(order.env, order.amount_total,
                                                                   currency_obj=order.currency_id)
            tax_totals['amount_timbre'] = formatLang(order.env, order.amount_timbre,
                                                          currency_obj=order.currency_id)
            order.tax_totals=tax_totals

    @api.model
    def _prepare_invoice(self):
        res = super(TimbrePurchases, self)._prepare_invoice()
        res['if_timbre'] = self.if_timbre
        res['txt_timbre'] = self.txt_timbre
        return res


