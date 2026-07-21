from odoo import _, api, fields, models


class TechflexContactRequest(models.Model):
    _name = "techflex.contact.request"
    _description = "TechFlex Contact Request"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "create_date desc"

    name = fields.Char(default=lambda self: _("New"), copy=False, readonly=True, tracking=True)
    state = fields.Selection(
        [("new", "New"), ("in_progress", "In Progress"), ("done", "Resolved")],
        default="new",
        tracking=True,
    )
    full_name = fields.Char(required=True)
    email = fields.Char(required=True)
    phone = fields.Char(required=True)
    subject = fields.Char(required=True)
    department = fields.Selection(
        [
            ("sales", "Sales"),
            ("rentals", "Rentals"),
            ("orders", "Orders & Delivery"),
            ("support", "Support & Advice"),
            ("general", "General Enquiry"),
        ],
        required=True,
    )
    message = fields.Text(required=True)
    website_id = fields.Many2one("website", readonly=True)
    submitted_from_website = fields.Boolean(default=False, readonly=True)

    @api.model_create_multi
    def create(self, vals_list):
        sequence = self.env["ir.sequence"]
        for vals in vals_list:
            if vals.get("name", _("New")) == _("New"):
                vals["name"] = sequence.next_by_code("techflex.contact.request") or _("New")
        return super().create(vals_list)
