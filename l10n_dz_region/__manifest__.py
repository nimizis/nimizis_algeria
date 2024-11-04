
{
    'name': 'Algeria - Regions',
    'version': '1.5',
    'description': """ 
    
Added some functionality (specific algeria):

    -   DATA of municipalities
    -   DATA of Wilaya
    -   Postal addresses
    -   Mandatory fields for Algerian legislation ( NIS AI..)
    -   the functionality of displaying these fields under the addresses
...""",
    'summary': 'Regions of Algeria',
    'author': 'NIMIZIS',
    'website': 'nimizis.com',
    'maintainer': 'hm@nimizis.com',
    'license': 'AGPL-3',
    'category': 'Tools',
    'post_init_hook': 'post_install',
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
