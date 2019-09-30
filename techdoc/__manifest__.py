# -*- coding: utf-8 -*-
# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full copyright and licensing details.
{
    'name': "TechDoc",
    'summary': "Technical Documentation.",
    'version': '0.1',
    'author': 'Nova Code',
    'website': "https://www.novacode.nl",
    'company': 'Nova Code',
    'category': 'Extra Tools',
    'depends': ['base'],
    'data': [
        'views/techdoc_view_form_field_views.xml',
        'views/techdoc_menu.xml',
        'wizard/techdoc_import.xml',
    ],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'description': """
Technical Documentation
=======================

- Generate form-view (UI) overview.
"""
}
