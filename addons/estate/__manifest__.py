{
    'name': "Real Estate",
    'version': '1.0',
    'depends': ['base'],
    'author': "Author Name",
    'category': 'Category',
    'description': """
    Description text
    """,
    'installable': True,
    'application': True,
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/estate_property_views.xml',
        'views/estate_property_offers.xml',
        'views/estate_property_tags.xml',
        'views/estate_property_type.xml',
        'views/estate_menus.xml',
        'views/inherited_res_users_views.xml',
    ],
}