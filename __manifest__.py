# -*- coding: utf-8 -*-
{
    'name': "intervention",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/collaborateur.xml',
        'views/parc.xml',
        'views/interlocuteur.xml',
        'views/site.xml',
        'views/statut.xml',
        'views/validation_plannif.xml',
        "views/type_intervention.xml",
        "views/article.xml",
        "views/defaut.xml",

    ],

}
