from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"
    _sql_constraints = [
        ('unique_property_type', 'unique(name)', 'Property type name must be unique.'),
    ]
    name = fields.Char(string=" Property Type", required=True)
    name = fields.Char("Name", required=True)
    sequence = fields.Integer("Sequence", default=10)
    property_ids = fields.One2many("estate.property", "property_type_id", string="Properties")