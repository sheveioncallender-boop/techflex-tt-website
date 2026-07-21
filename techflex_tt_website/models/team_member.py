from odoo import fields, models


class TechflexTeamMember(models.Model):
    _name = "techflex.team.member"
    _description = "TechFlex Team Member"
    _order = "sequence, id"

    name = fields.Char(required=True)
    job_title = fields.Char(required=True)
    short_bio = fields.Text()
    image_1920 = fields.Image(max_width=1920, max_height=1920)
    sequence = fields.Integer(default=10)
    active = fields.Boolean(default=True)
    website_id = fields.Many2one("website", string="Website")
