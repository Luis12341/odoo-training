from odoo import models, fields, api, exceptions
from dateutil.relativedelta import relativedelta
import logging
_logger = logging.getLogger(__name__) 

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = "Estate property offer"
    _order = "price desc"

    price = fields.Float(string="Precios")
    status = fields.Selection(
        [('accepted', 'Aceptada'), ('refused', 'Rechazada')], string="Estado", copy=False)
    partner_id = fields.Many2one(
        'res.partner', string="Comprador", required=True)
    property_id = fields.Many2one(
        'estate.property', string="Propiedad")
    date_deadline = fields.Date(
        string="Fecha de finalizacion", readonly=False,compute="_compute_date_deadline",inverse="_compute_validity")
    validity = fields.Integer(string="Dias para Finalizar", default=7)
    property_type_id = fields.Many2one('estate.property.type', string="Tipo de Propiedad", related='property_id.property_type_id')

    @api.depends("validity","date_deadline")
    def _compute_date_deadline(self):
        for offer in self:
            date = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.date_deadline = date + relativedelta(days=offer.validity)

    def _compute_validity(self):
        for offer in self:
            date = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.validity = (offer.date_deadline - date).days
    
    def action_accepted(self):
        self.status = 'accepted'
        self.property_id.state = 'offer_accepted'
        self.property_id.selling_price = self.price
        self.property_id.buyer_id = self.partner_id

    
    def action_refused(self):
        self.status = 'refused'
        
    @api.model
    def create(self, vals):
        property = self.env['estate.property'].browse(vals['property_id'])
        if property.state != 'offer_received':
            property.state = 'offer_received'
            
        if vals['price'] < property.expected_price: 
            raise exceptions.ValidationError("El precio de la oferta no puede ser menor al precio esperado")
        
        return super().create(vals)
        
            
    _sql_constraints = [
        ('check_price', 'CHECK(price > 0)', 'El precio de oferta es incorrecto'),   
    ]