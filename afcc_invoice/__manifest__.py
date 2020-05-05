# -*- coding: utf-8 -*-
{
    'name' : 'AFCC Combined Invoice Report',
    'version' : '12.0.1',
    'summary': 'Custom invoice Report',
    'sequence': 16,
    'category': 'Sales',
    'author' : 'Magdy,TeleNoc',
    'description': """
    Custom invoice Report
    """,
    "license": "AGPL-3",
    'depends' : ['base','sale', 'account', 'afcc_transportation'],
    'data': [
        # 'wizard/wiz_periodical_report_view.xml',
        # 'views/periodical_report.xml',
        'views/report_periodical_sales.xml',
        'views/invoice_report.xml',
        'views/sale_order_report.xml'
    ],
    # 'images': [
    #     'static/description/banner.jpg'
    # ],
    # 'installable': True,
    # 'application': True,
    # 'auto_install': False,
}
