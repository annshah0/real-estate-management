from odoo import models, fields

class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Property Tags'
    _sql_constraints = [
        ('unique_property_tag', 'unique(name)', 'Property tag name must be unique.'),
    ]
    name = fields.Char(string='Name', required=True)
    color = fields.Integer("Color Index")

