from datetime import datetime, timedelta
from odoo import api, fields, models
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare, float_is_zero

class EstateProperties(models.Model):
    _name = "estate.property"
    _description = "Model for Real-Estate Properties"
    name = fields.Char(string="Title", required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date("Available From", default=lambda self: self._default_date_availability(),copy=False)
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price", copy=False, readonly=True)
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area(sqm)")
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West'),
    ], string="Garden Orientation")
    _sql_constraints = [
        ('check_expected_price', 'CHECK (expected_price > 0)', 'Expected price must be strictly positive'),
        ('check_selling_price', 'CHECK (selling_price >= 0)', 'Selling price must be positive'),
    ]

    def _default_date_availability(self):
        return fields.Date.context_today(self) + relativedelta(months=3)

#state field
    state = fields.Selection([
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('offer_refused', 'Offer Refused'),
        ('sold', 'Sold'),
        ('canceled', 'Canceled'),
    ], string="Status", default='new', required=True, copy=False, tracking=True,)


#property types
    property_type_id = fields.Many2one('estate.property.type', string="Property Type", required=True)
    buyer_id = fields.Many2one('res.partner', string="Buyer", readonly=True,copy=False)
    seller_id = fields.Many2one('res.users', string="Salesman", default=lambda self: self.env.user)

#tags

    tag_ids = fields.Many2many("estate.property.tag", string="Tags")

#offer
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers')

#total area and best offer
    total_area = fields.Float(compute="_compute_total_area", string="Total Area")
    best_offer = fields.Float(compute="_compute_best_offer", string="Best Offer")

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = int(record.living_area + record.garden_area)

    @api.depends("offer_ids.price")
    def _compute_best_offer(self):
        for record in self:
            best_offer = max(record.offer_ids.mapped("price"), default=0)
            record.best_offer = best_offer

#onchange garden

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = False
            self.garden_orientation = False

#property cancelled or sold

    def action_sold(self):
        if any(prop.state == "canceled" for prop in self):
            raise UserError("Canceled properties cannot be sold.")
        return self.write({"state": "sold"})

    def action_cancel(self):
        if any(prop.state == "sold" for prop in self):
            raise UserError("Sold properties cannot be canceled.")
        return self.write({"state": "canceled"})

#python constraint

    @api.constrains("expected_price", "selling_price")
    def _check_selling_price(self):
        for property in self:
            if (
                    not float_is_zero(property.selling_price, precision_digits=2)
                    and property.expected_price
                    and float_compare(
                property.selling_price, property.expected_price * 0.9, precision_digits=2
            ) == -1
            ):
                raise models.ValidationError(
                    "Selling price cannot be lower than 90% of the expected price!"
                )

