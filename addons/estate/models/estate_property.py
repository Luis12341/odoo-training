from odoo import models, fields, api, exceptions
from odoo.tools import float_is_zero, float_compare
import logging
_logger = logging.getLogger(__name__)


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"
    _order = "id desc"

    name = fields.Char(string="Nombre", required=True)
    description = fields.Text(string="Descripción")
    postcode = fields.Char(string="Código Postal")
    date_availability = fields.Date(
        string="Fecha Disponible", copy=False, default=lambda self: fields.Date.today())
    expected_price = fields.Float(string="Precio Esperado", required=True)
    selling_price = fields.Float(string="Precio de Venta", readonly=True)
    bedrooms = fields.Integer(string="Dormitorios", default=2)
    living_area = fields.Integer(string="Área de Vivienda")
    facades = fields.Integer(string="Fachadas")
    garage = fields.Boolean(string="Garaje")
    garden = fields.Boolean(string="Jardín")
    garden_area = fields.Integer(string="Área de Jardín")
    garden_orientation = fields.Selection(
        [('N', 'Norte'), ('S', 'Sur'), ('E', 'Este'), ('O', 'Oeste')], string="Orientación de Jardín")
    active = fields.Boolean(string="Activo", default=True)
    state = fields.Selection([('new', 'Nuevo'), ('offer_received', 'Oferta Recibida'), ('offer_accepted',
                             'Oferta Aceptada'), ('sold', 'Vendida'), ('canceled', 'Cancelada')], string="Estado", default='new', readonly=True)

    best_price = fields.Float(string="Mejor Precio",
                              compute="_compute_best_price", readonly=True)
    property_type_id = fields.Many2one(
        'estate.property.type', string="Tipo de Propiedad")
    salesperson_id = fields.Many2one(
        'res.users', string="Vendedor", copy=False, default=lambda self: self.env.user)
    buyer_id = fields.Many2one('res.partner', string="Comprador", copy=False)
    tags_ids = fields.Many2many('estate.property.tag', string="Etiquetas")
    offers_ids = fields.One2many(
        'estate.property.offer', 'property_id', string="Oferta")

    total_area = fields.Integer(
        string="Area Total", readonly=True, compute="_compute_total_area")

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('expected_price', 'offers_ids')
    def _compute_best_price(self):
        for record in self:
            record.best_price = record.expected_price
            for offer in record.offers_ids:
                if offer.price > record.best_price:
                    record.best_price = offer.price

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'N'
        else:
            self.garden_area = 0
            self.garden_orientation = ''

    @api.depends("offers_ids")
    def _onchange_offers_ids(self):
        for record in self:
            if len(record.offers_ids) > 0:
                record.state = 'offer_received'

    def property_sold(self):
        for record in self:
            if record.state != 'sold' and record.state != 'canceled':
                record.state = 'sold'
        return True

    def property_cancel(self):
        for record in self:
            if record.state != 'canceled' and record.state != 'sold':
                record.state = 'canceled'
        return True

    @api.constrains('expected_price', 'selling_price')
    def _constraint_price(self):
        for record in self:
            if not float_is_zero(record.selling_price, 3) and float_compare(record.selling_price, record.expected_price * 0.9, 3) < 0:
                raise exceptions.ValidationError(
                    'El precio debe ser mayor o igual al 90% del valor de la propiedad')

    def unlink(self):
        for record in self:
            if record.state not in ['new', 'canceled']:
                raise exceptions.UserError(
                    'No se puede eliminar una propiedad que ya ha sido vendida o cancelada')

        return super().unlink()

    _sql_constraints = [
        ('check_expected_price_property', 'CHECK(expected_price > 0)',
         'El precio esperado es incorrecto'),
        ('check_selling_price_property', 'CHECK(selling_price > 0)',
         'El precio de venta es incorrecto'),
    ]
