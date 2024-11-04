# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
#
# Copyright (c) 2024  - NiMiZiS - www.nimizis.com
#                                                hm@nimizis.com

from odoo import fields, models, api
from collections import defaultdict
import re

ADDRESS_FIELDS = ('street', 'street2', 'zip', 'city', 'state_id', 'country_id', 'vat', 'nis','company_registry','ai','commune_id')


class ResPartner(models.Model):
    _inherit = 'res.partner'

    commune_id = fields.Many2one('res.commune', string='Commune',domain="[('state_id', '=?', state_id)]", track_visibility='onchange')
    region_id = fields.Many2one('res.region', string='Region',related='state_id.region_id', store=True, readonly=True)
    country_id = fields.Many2one('res.country', string='Country', required=True,default=lambda self: self.env.ref('base.dz'), track_visibility='onchange')
    nis = fields.Char(string='N.I.S', track_visibility='onchange')
    ai = fields.Char(string='Article d\'imposition', track_visibility='onchange')
    forme_juridique_id = fields.Many2one('forme.juridique', string='Forme juridique', track_visibility='onchange')
    share_capital = fields.Float('Capital Social', track_visibility='onchange')




    @api.model
    def _address_fields(self):
        """Returns the list of address fields that are synced from the parent."""
        return list(ADDRESS_FIELDS)



    @api.model
    def _get_default_address_format(self):
        return "%(street)s\n%(street2)s\n%(city)s %(commune)s %(zip)s\n%(state_name)s %(country_name)s\nRC : %(rc)s\nNIF : %(nif)s\nNIS : %(nis)s\nAI : %(ai)s"

    def _display_address_depends(self):
        # field dependencies of method _display_address()
        return self._formatting_address_fields() + [
            'country_id', 'company_name', 'state_id', 'vat', 'nis','company_registry','ai','commune_id'
        ]

    def _prepare_display_address(self, without_company=False):
        # get the information that will be injected into the display format
        # get the address format
        address_format = self._get_address_format()
        args = defaultdict(str, {
            'state_code': self.state_id.code or '',
            'state_name': self.state_id.name or '',
            'country_code': self.country_id.code or '',
            'country_name': self._get_country_name(),
            'commune': self.commune_id.name or '',
            'rc': self.company_registry or '',
            'nif': self.vat or '',
            'nis': self.nis or '',
            'ai': self.ai or '',
        })
        for field in self._formatting_address_fields():
            args[field] = self[field] or ''
        if without_company:
            args['company_name'] = ''
        elif self.commercial_company_name:
            address_format = '%(company_name)s\n' + address_format
        return address_format, args

    @api.depends('company_name','forme_juridique_id', 'parent_id.is_company', 'commercial_partner_id.name')
    def _compute_commercial_company_name(self):
        for partner in self:
            p = partner.commercial_partner_id
            if p.forme_juridique_id:
                partner.commercial_company_name = p.is_company and p.forme_juridique_id.name+" "+p.name or partner.company_name
            else:
                partner.commercial_company_name = p.is_company and p.name or partner.company_name

    def _get_name(self):
        """ Utility method to allow name_get to be overrided without re-browse the partner """
        partner = self
        name = partner.name or ''
        if partner.company_name or partner.parent_id:
            if not name and partner.type in ['invoice', 'delivery', 'other']:
                types = dict(self._fields['type']._description_selection(self.env))
                name = types[partner.type]
            if not partner.is_company:
                name = self._get_contact_name(partner, name)
        if self._context.get('show_address_only'):
            name = partner._display_address(without_company=True)
        if self._context.get('show_address'):
            name = name + "\n" + partner._display_address(without_company=True)
        name = re.sub(r'\s+\n', '\n', name)
        if self._context.get('partner_show_db_id'):
            name = "%s (%s)" % (name, partner.id)
        if self._context.get('address_inline'):
            splitted_names = name.split("\n")
            name = ", ".join([n for n in splitted_names if n.strip()])
        if self._context.get('show_email') and partner.email:
            name = "%s <%s>" % (name, partner.email)
        if self._context.get('html_format'):
            name = name.replace('\n', '<br/>')
        if partner.forme_juridique_id:
            name = "%s  %s" % ( partner.forme_juridique_id.name,name)
        return name.strip()

    @api.onchange('commune_id')
    def commune_id_change(self):
        for partner in self:
            if partner.commune_id:
                partner.state_id = partner.commune_id.state_id.id
                if 'X' in partner.commune_id.code:
                    partner.zip=partner.state_id.code
                else:
                    partner.zip=partner.state_id.code+partner.commune_id.code