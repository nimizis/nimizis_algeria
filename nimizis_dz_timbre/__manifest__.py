# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
#
# Copyright (c) 2024  - NiMiZiS - www.nimizis.com
#                                                hm@nimizis.com
{
    "name": "Algeria - Timbre fiscal",
    "summary": "Module to add Timbre tax (for ALGERIA)",
    "version": "1.3",
    'website': 'https://nimizis.com',
    "author": "NiMiZiS",
    'maintainer': 'hm@nimizis.com',
    "license": "AGPL-3",
    "depends": [ 'l10n_dz','purchase', 'sale' ],
    'category': 'Accounting/Localizations',

    'images': ['static/description/Nimizis dz timbre.gif'],

    'data': [
        'views/res_config_timbre_view.xml',
        'views/account_move_view.xml',
        'views/purchase_order_view.xml',
        'views/sale_order_view.xml',

        'reports/report_invoice.xml',
        'reports/report_sale_order.xml',
        'reports/report_purchase_order.xml',
    ],
}
