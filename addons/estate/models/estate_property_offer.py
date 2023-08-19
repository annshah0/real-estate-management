from odoo import api, models, fields
from dateutil.relativedelta import relativedelta


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Real Estate Property Offer'
    _sql_constraints = [
        ('check_offer_price', 'CHECK (price >= 0)', 'Offer price must be positive.'),
    ]

    price = fields.Float(string='Price', required=True)
    state = fields.Selection(
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused"),],string="Status",copy=False,default=False,)
    partner_id = fields.Many2one('res.partner', string='Partner', required=True, domain="[('customer', '=', True)]")
    property_id = fields.Many2one('estate.property', string='Property', required=True)
    property_type_id = fields.Many2one(
        "estate.property.type", related="property_id.property_type_id", string="Property Type", store=True)
 #offer

    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(string="Deadline Date", compute="_compute_date_deadline",inverse="_inverse_date_deadline")

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for offer in self:
            date = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.date_deadline = date + relativedelta(days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            date = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.validity = (offer.date_deadline - date).days

#accept or refuse offer

    def action_accept(self):
        self.write({
            "state": "accepted",
        })
        self.mapped("property_id").write({
            "state": "offer_accepted",
            "selling_price": self.price,
            "buyer_id": self.partner_id.id,
        })


    def action_refuse(self):
        self.write({
            "state": "refused",
        })
        self.mapped("property_id").write({
            "state": "offer_refused",
        })