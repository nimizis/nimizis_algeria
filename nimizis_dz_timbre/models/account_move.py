# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
#
# Copyright (c) 2024  - NiMiZiS - www.nimizis.com
#                                                hm@nimizis.com
from odoo import api, exceptions, fields, models, tools, Command, _
from odoo.exceptions import ValidationError, UserError
from contextlib import ExitStack, contextmanager
import logging

_logger = logging.getLogger(__name__)
import math


class AccountInvoiceTimbre(models.Model):
    _inherit = "account.move"

    if_timbre = fields.Boolean(string='Timbre ?', default=False,readonly=True,)
    amount_timbre = fields.Monetary(string='Montant du Timbre', readonly=True,store=1,tracking=True)

    # the function that applies the stamp on the invoice
    def add_timbre(self):
        self.write({'if_timbre': True})
        for rec in self:
            total_tax_currency, total_untaxed_currency = 0.0, 0.0
            if rec.is_invoice(True) and rec.if_timbre and rec.line_ids:
                # === Invoices ===
                for line in rec.line_ids:
                    if line.display_type == 'tax' or (line.display_type == 'rounding' and line.tax_repartition_line_id):
                        # Tax amount.
                        total_tax_currency += line.amount_currency
                    elif line.display_type in ('product', 'rounding'):
                        # Untaxed amount.
                        total_untaxed_currency += line.amount_currency
                total_untaxed_currency=total_untaxed_currency*rec.direction_sign
                total_tax_currency=total_tax_currency*rec.direction_sign
                amount_timbre = math.ceil(((total_tax_currency+total_untaxed_currency) * rec.company_id.prcent) / 100)
                if amount_timbre < rec.company_id.timbre_min:
                    amount_timbre = rec.company_id.timbre_min
                elif amount_timbre > rec.company_id.timbre_max:
                    amount_timbre = rec.company_id.timbre_max
                rec.amount_timbre = amount_timbre
                if  (rec.move_type == "out_invoice" or rec.move_type == "out_refund"):
                    already_exists = rec.line_ids.filtered(lambda line: line.name and line.account_id == rec.company_id.sales_timbre_account_id)
                if  (rec.move_type == "in_invoice" or rec.move_type == "in_refund"):
                    already_exists = rec.line_ids.filtered(lambda line: line.name and line.account_id == rec.company_id.purchase_timbre_account_id)
                if already_exists:
                    if  (rec.move_type == "out_invoice" or rec.move_type == "out_refund"):
                        already_exists.update({'name': "TIMBRE FISCAL",'credit': amount_timbre })
                    if (rec.move_type == "in_invoice" or rec.move_type == "in_refund"):
                        already_exists.update({'name': "TIMBRE FISCAL",'debit': amount_timbre })
                else:
                    if rec.move_type == "out_invoice" :
                        dict = {
                            'move_name': rec.name+" TIMBRE",
                            'name': 'TIMBRE FISCAL',
                            'quantity': 1,
                            'credit': amount_timbre ,
                            'account_id': rec.company_id.sales_timbre_account_id.id,
                            'move_id': rec._origin.id,
                            'currency_id': rec.currency_id.id,
                            'date': rec.date,
                            'display_type':'tax',
                            'partner_id': rec.partner_id.id,
                            'company_id': rec.company_id.id,
                            'company_currency_id': rec.company_currency_id.id,
                            }
                    elif  rec.move_type == "out_refund":
                        dict = {
                            'move_name': rec.name+" TIMBRE",
                            'name': 'TIMBRE FISCAL',
                            'quantity': 1,
                            'debit': amount_timbre ,
                            'account_id': rec.company_id.sales_timbre_account_id.id,
                            'move_id': rec._origin.id,
                            'currency_id': rec.currency_id.id,
                            'date': rec.date,
                            'display_type':'tax',
                            'partner_id': rec.partner_id.id,
                            'company_id': rec.company_id.id,
                            'company_currency_id': rec.company_currency_id.id,
                            }
                    elif rec.move_type == "in_invoice":
                        dict = {
                            'move_name': rec.name+" TIMBRE",
                            'name': 'TIMBRE FISCAL',
                            'quantity': 1,
                            'debit': amount_timbre ,
                            'account_id': rec.company_id.purchase_timbre_account_id.id,
                            'move_id': rec._origin.id,
                            'currency_id': rec.currency_id.id,
                            'date': rec.date,
                            'sequence': True,
                            'display_type': 'tax',
                            'partner_id': rec.partner_id.id,
                            'company_id': rec.company_id.id,
                            'company_currency_id': rec.company_currency_id.id,
                            }
                    elif rec.move_type == "in_refund":
                        dict = {
                            'move_name': rec.name+" TIMBRE",
                            'name': 'TIMBRE FISCAL',
                            'quantity': 1,
                            'credit': amount_timbre ,
                            'account_id': rec.company_id.purchase_timbre_account_id.id,
                            'move_id': rec._origin.id,
                            'currency_id': rec.currency_id.id,
                            'date': rec.date,
                            'sequence': True,
                            'display_type': 'tax',
                            'partner_id': rec.partner_id.id,
                            'company_id': rec.company_id.id,
                            'company_currency_id': rec.company_currency_id.id,
                            }
                    create_method =  rec.env['account.move.line'].create
                    rec.line_ids += create_method(dict)

    # applied the function of adding the stamp when creating an invoice with stamp (from an order)
    @api.model_create_multi
    def create(self, vals_list):
        res = super(AccountInvoiceTimbre, self).create(vals_list)
        for inv in res:
            if inv.if_timbre:
                inv.add_timbre()
        return res

    # the function that removes the stamp application from the invoice
    def del_timbre(self):
        self.if_timbre = False
        self.amount_timbre = 0
        already_exists = False
        if (self.move_type == "out_invoice" or self.move_type == "out_refund"):
            already_exists = self.line_ids.filtered(
                lambda line: line.name and line.account_id == self.company_id.sales_timbre_account_id)
        if (self.move_type == "in_invoice" or self.move_type == "in_refund"):
            already_exists = self.line_ids.filtered(
                lambda line: line.name and line.account_id == self.company_id.purchase_timbre_account_id)
        if already_exists:
            self.line_ids -= already_exists


    # in case of modification after the application of stamp duty
    @api.onchange('invoice_line_ids','partner_id','line_ids','currency_id','if_timbre')
    def annul_timbre(self):
        if self.if_timbre:
            self.del_timbre()



class AccountMoveLineTimbre(models.Model):
    _inherit = "account.move.line"

    # add permission to delete stamp tax lines
    @api.ondelete(at_uninstall=False)
    def _prevent_automatic_line_deletion(self):
        if not self.env.context.get('dynamic_unlink'):
            for line in self:
                if line.display_type == 'tax' and line.move_id.line_ids.tax_ids:
                    if line.account_id!=line.company_id.purchase_timbre_account_id and line.account_id!=line.company_id.sales_timbre_account_id :
                        raise ValidationError(_(
                        "You cannot delete a tax line as it would impact the tax report"
                    ))
                elif line.display_type == 'payment_term':
                    raise ValidationError(_(
                        "You cannot delete a payable/receivable line as it would not be consistent "
                        "with the payment terms"
                    ))
