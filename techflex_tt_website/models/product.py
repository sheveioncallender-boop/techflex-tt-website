from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    techflex_monthly_special = fields.Boolean(
        string="Monthly Special",
        help="Show this published product in the TechFlex homepage Monthly Specials section.",
    )
    techflex_condition = fields.Selection(
        [
            ("new", "Brand New"),
            ("renewed", "TechFlex Renewed"),
            ("refurbished", "Professionally Refurbished"),
            ("open_box", "Open Box"),
        ],
        string="Product Condition",
    )
    techflex_warranty_label = fields.Char(
        string="Warranty Label",
        help="Example: 1 Year Manufacturer Warranty",
    )
    techflex_warranty_months = fields.Integer(string="Warranty Duration (Months)")
    techflex_warranty_details = fields.Html(string="Warranty & Support Details")
    techflex_support_note = fields.Text(string="Support Note")
    techflex_delivery_note = fields.Text(string="Delivery Note")
    techflex_show_details = fields.Boolean(string="Show TechFlex Detail Sections", default=True)
    techflex_spec_line_ids = fields.One2many(
        "techflex.product.spec.line", "product_tmpl_id", string="Technical Specifications"
    )
    techflex_highlight_line_ids = fields.One2many(
        "techflex.product.highlight", "product_tmpl_id", string="Key Highlights"
    )


class TechflexProductSpecLine(models.Model):
    _name = "techflex.product.spec.line"
    _description = "TechFlex Product Specification"
    _order = "sequence, id"

    sequence = fields.Integer(default=10)
    product_tmpl_id = fields.Many2one(
        "product.template", required=True, ondelete="cascade", index=True
    )
    section = fields.Char(default="Specifications")
    name = fields.Char(string="Specification", required=True)
    value = fields.Char(required=True)
    show_on_website = fields.Boolean(default=True)


class TechflexProductHighlight(models.Model):
    _name = "techflex.product.highlight"
    _description = "TechFlex Product Highlight"
    _order = "sequence, id"

    sequence = fields.Integer(default=10)
    product_tmpl_id = fields.Many2one(
        "product.template", required=True, ondelete="cascade", index=True
    )
    name = fields.Char(string="Highlight", required=True)
