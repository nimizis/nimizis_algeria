
{
    'name': 'Algeria - Base',
    'version': '1.7',

    'author': 'NIMIZIS',
    'website': 'https://nimizis.com',
    'maintainer': 'hm@nimizis.com',
    'license': 'AGPL-3',
    'category': 'Localization',
    'post_init_hook': 'post_install',
    'images': ['static/description/banner.gif'],
    'depends': [
        'contacts'
    ],
    'data': [
        'security/ir.model.access.csv',

        'data/forme_juridique.xml',
        'data/res_country.xml',
        'data/wilaya.xml',
        'data/commune.xml',

        'views/forme_juridique.xml',
        'views/res_commune.xml',
        'views/res_state.xml',
        'views/res_region.xml',
        'views/res_partner.xml',
        'views/res_company.xml',

        'menu.xml',

    ]
}
