from odoo import models, fields

class EstateProperty(models.Model):
    _name="estate.property"
    _description="Real Estate Property"
    
    name = fields.Char(name="Nombre",required=True)
    description = fields.Text(name="Descripción")
    postcode = fields.Char(name="Código Postal")
    date_availability = fields.Date(name="Fecha Disponible")
    expected_price = fields.Float(name="Precio Esperado",required=True)
    selling_price = fields.Float(name="Precio de Venta")
    bedrooms = fields.Integer(name="Dormitorios")
    living_area = fields.Integer(name="Área de Vivienda")
    facades = fields.Integer(name="Fachadas")
    garage = fields.Integer(name="Garaje")
    garden = fields.Integer(name="Jardín")
    garden_area = fields.Integer(name="Área de Jardín")
    garden_orientation = fields.Selection([('N','Norte'),('S','Sur'),('E','Este'),('O','Oeste')], name="Orientación de Jardín")