from odoo import models, fields

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Real Estate Property Tag"
    _order = "name asc"

    name = fields.Char(string="Nombre", required=True)
    color = fields.Integer(string="Color")
    
    _sql_constraints = [
        ('name_uniq', 'unique (name)', 'La etiqueta ya existe'),
    ]