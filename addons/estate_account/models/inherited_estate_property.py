from odoo import api, fields, models, exceptions
import logging
_logger = logging.getLogger(__name__)


class InheritedEstateProperty(models.Model):
    _inherit = 'estate.property'

    def property_sold(self):
        move_type = 'out_invoice'
        journal_id = self.env['account.journal'].search(
            [('type', '=', 'sale')], limit=1)
        for record in self:
            partner_id = record.buyer_id.id
            self.env['account.move'].create(
                {"partner_id": partner_id, "move_type": move_type, "journal_id": journal_id.id, "invoice_line_ids": [
                    (
                        0,
                        0,
                        {
                            "name": record.name,
                            "quantity": 1.0,
                            "price_unit": record.selling_price * (6 / 100),
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "name": "Comision administrativa",
                            "quantity": 1.0,
                            "price_unit": 100.0,
                        },
                    )
                ]})
        return super(InheritedEstateProperty, self).property_sold()
