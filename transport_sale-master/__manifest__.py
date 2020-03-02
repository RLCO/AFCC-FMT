# {
#     "name": "Transport sale",
#     "version": "1.0",
#     "depends": ["base","fleet","sale","hr"],
#     "author": "Alien Group Lda",
#     'website':'http://www.alien-group.com',
#     "category": "Sales Management",
#     "description": """
#     This module provide :
#     Vehicles that executed a transport sales order in the sale order
#     All sales by each vehicle in Vehicles form
#     All sales by each vehicle driver in employee form
#     """,
#     'data':['transport_sale.xml','security/ir.model.access.csv'],
#     'installable': True,
#
# }
{
    'name': "Transport sale",

    'summary': """
        Transport""",

    'description': """
       Transport
    """,

    'author': "Telenoc",
    'website': "https:www.telenoc.org",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ["base","fleet","sale","hr"],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/transport_sale.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}