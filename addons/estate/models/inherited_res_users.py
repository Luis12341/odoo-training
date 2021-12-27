from odoo import models, fields, api, exceptions

class VendorProperties(models.Model):
    _inherit = 'res.users'
    
    property_ids = fields.One2many('estate.property', 'salesperson_id', string="Propiedades", domain=[('state', 'in', ['new','offer_received'])])