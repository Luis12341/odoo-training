from odoo import models, fields, api

class EstatePropertyType(models.Model):
    _name="estate.property.type"
    _description="Real Estate Property Type"
    _order = "secuence, name"
    
    name = fields.Char(string="Nombre",required=True)
    properties_ids = fields.One2many("estate.property","property_type_id",string="Propiedades")
    secuence = fields.Integer(string="Secuencia",default=1)
    
    offer_ids = fields.One2many("estate.property.offer","property_type_id",string="Ofertas")
    offer_count = fields.Integer(string="Cantidad de Ofertas",compute="_compute_offer_count")
    
    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
    
    _sql_constraints = [
        ('name_uniq', 'unique (name)', 'El tipo de propiedad ya existe'),
    ]