from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class TechflexRentalRequest(models.Model):
    _name = "techflex.rental.request"
    _description = "TechFlex Rental Request"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "create_date desc"

    name = fields.Char(default=lambda self: _("New"), copy=False, readonly=True, tracking=True)
    state = fields.Selection(
        [
            ("new", "New"),
            ("contacted", "Contacted"),
            ("quoted", "Quoted"),
            ("confirmed", "Confirmed"),
            ("done", "Completed"),
            ("cancelled", "Cancelled"),
        ],
        default="new",
        tracking=True,
    )
    first_name = fields.Char(required=True)
    last_name = fields.Char(required=True)
    company_name = fields.Char()
    email = fields.Char(required=True)
    phone = fields.Char(required=True)
    business_address = fields.Text(required=True)
    equipment_desktops = fields.Boolean(string="Desktops")
    equipment_laptops = fields.Boolean(string="Laptops")
    equipment_tablets = fields.Boolean(string="Tablets")
    equipment_tvs = fields.Boolean(string="TVs / Monitors")
    equipment_projectors = fields.Boolean(string="Projectors")
    equipment_printers = fields.Boolean(string="Printers")
    equipment_accessories = fields.Boolean(string="Accessories / Peripherals")
    equipment_other = fields.Char(string="Other Equipment")
    specification_level = fields.Selection(
        [("basic", "Basic"), ("mid", "Mid Range"), ("high", "High End")],
        required=True,
    )
    number_of_units = fields.Integer(required=True, default=1)
    rental_start_date = fields.Date(required=True)
    rental_end_date = fields.Date()
    rental_duration = fields.Char()
    pickup_delivery = fields.Selection(
        [("pickup", "Pickup"), ("delivery", "Delivery"), ("either", "Either")],
        required=True,
    )
    additional_info = fields.Text()
    website_id = fields.Many2one("website", readonly=True)
    submitted_from_website = fields.Boolean(default=False, readonly=True)

    @api.constrains("number_of_units")
    def _check_number_of_units(self):
        for rental in self:
            if not 1 <= rental.number_of_units <= 65:
                raise ValidationError(_("The number of rental units must be between 1 and 65."))

    @api.constrains("rental_start_date", "rental_end_date")
    def _check_rental_dates(self):
        for rental in self:
            if (
                rental.rental_start_date
                and rental.rental_end_date
                and rental.rental_end_date < rental.rental_start_date
            ):
                raise ValidationError(_("The rental end date cannot be before the start date."))

    @api.model_create_multi
    def create(self, vals_list):
        sequence = self.env["ir.sequence"]
        for vals in vals_list:
            if vals.get("name", _("New")) == _("New"):
                vals["name"] = sequence.next_by_code("techflex.rental.request") or _("New")
        return super().create(vals_list)
