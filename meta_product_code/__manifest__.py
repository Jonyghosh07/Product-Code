{
    'name': 'Auto Product Internal Reference Code',
    'version': '17.0.1.0.0',
    'category': 'Inventory/Products',
    'summary': 'Manage product codes and references',
    'description': """
        This module provides functionality to manage product codes:
        * Generate unique product codes
        * Track and manage product references
        * Custom product code formats
    """,
    'author': 'Jony Ghosh',

    'depends': [
        'base',
        'product',
    ],
    'data': [
        'views/category_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'OPL-1',
    
    "maintainer": "Jony Ghosh",
    "support": "jony.ghosh98@gmail.com",
}