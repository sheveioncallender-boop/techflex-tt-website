from odoo import fields, models


class TechflexLocation(models.Model):
    _name = "techflex.location"
    _description = "TechFlex Location"
    _order = "sequence, id"

    name = fields.Char(required=True)
    island = fields.Selection([("trinidad", "Trinidad"), ("tobago", "Tobago")])
    address = fields.Text(required=True)
    phone = fields.Char()
    email = fields.Char()
    business_hours = fields.Text()
    map_url = fields.Char()
    image_1920 = fields.Image(max_width=1920, max_height=1920)
    sequence = fields.Integer(default=10)
    active = fields.Boolean(default=True)
    website_id = fields.Many2one("website", string="Website")
