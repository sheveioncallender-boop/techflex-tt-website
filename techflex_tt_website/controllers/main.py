from odoo import fields, http
from odoo.http import request
from odoo.fields import Domain
from odoo.addons.website.controllers.main import Website


class TechflexWebsiteController(Website):
    """Public routes for the TechFlex website.

    The controller extends Odoo's native Website controller so the root route is
    overridden cleanly while the rest of Odoo's website and eCommerce routes
    continue to operate normally.
    """

    def _website_record_domain(self):
        """Return shared records or records assigned to the current website."""
        return [
            ("active", "=", True),
            "|",
            ("website_id", "=", False),
            ("website_id", "=", request.website.id),
        ]

    def _page_values(self, **extra):
        values = {
            "team_members": request.env["techflex.team.member"].sudo().search(
                self._website_record_domain(), order="sequence, id", limit=9
            ),
            "locations": request.env["techflex.location"].sudo().search(
                self._website_record_domain(), order="sequence, id"
            ),
        }
        values.update(extra)
        return values

    @http.route()
    def index(self, **kw):
        """Render the TechFlex homepage at Odoo's native root route."""
        Product = request.env["product.template"].sudo().with_context(
            website_id=request.website.id,
            pricelist=request.pricelist.id,
            quantity=1,
        )
        base_domain = Domain(request.website.sale_product_domain())
        specials = Product.search(
            base_domain & Domain("techflex_monthly_special", "=", True),
            order="write_date desc, id desc",
            limit=5,
        )
        if not specials:
            specials = Product.search(
                base_domain,
                order="write_date desc, id desc",
                limit=5,
            )
        special_prices = specials._get_sales_prices(request.website) if specials else {}
        return request.render(
            "techflex_tt_website.page_home",
            self._page_values(
                monthly_specials=specials,
                monthly_special_prices=special_prices,
            ),
        )

    @http.route("/rentals", type="http", auth="public", website=True, sitemap=True)
    def rentals(self, **kwargs):
        return request.render(
            "techflex_tt_website.page_rentals",
            self._page_values(
                submitted=kwargs.get("submitted"),
                error=kwargs.get("error"),
            ),
        )

    @http.route("/about-us", type="http", auth="public", website=True, sitemap=True)
    def about_us(self, **kwargs):
        return request.render("techflex_tt_website.page_about", self._page_values())

    @http.route("/contact-us", type="http", auth="public", website=True, sitemap=True)
    def contact_us(self, **kwargs):
        return request.render(
            "techflex_tt_website.page_contact",
            self._page_values(
                submitted=kwargs.get("submitted"),
                error=kwargs.get("error"),
            ),
        )

    @http.route(
        "/techflex/rental/submit",
        type="http",
        auth="public",
        methods=["POST"],
        website=True,
        csrf=True,
        sitemap=False,
    )
    def rental_submit(self, **post):
        required = [
            "first_name",
            "last_name",
            "email",
            "phone",
            "business_address",
            "specification_level",
            "number_of_units",
            "rental_start_date",
            "pickup_delivery",
        ]
        if any(not post.get(field) for field in required):
            return request.redirect("/rentals?error=missing")

        equipment_fields = [
            "equipment_desktops",
            "equipment_laptops",
            "equipment_tablets",
            "equipment_tvs",
            "equipment_projectors",
            "equipment_printers",
            "equipment_accessories",
        ]
        if not any(post.get(field) for field in equipment_fields) and not post.get(
            "equipment_other"
        ):
            return request.redirect("/rentals?error=equipment")

        specification_level = post.get("specification_level")
        pickup_delivery = post.get("pickup_delivery")
        if specification_level not in {"basic", "mid", "high"}:
            return request.redirect("/rentals?error=specification")
        if pickup_delivery not in {"pickup", "delivery", "either"}:
            return request.redirect("/rentals?error=delivery")

        try:
            units = int(post.get("number_of_units", 1))
            if units < 1 or units > 65:
                raise ValueError
        except (TypeError, ValueError):
            return request.redirect("/rentals?error=units")

        try:
            rental_start_date = fields.Date.to_date(post.get("rental_start_date"))
            rental_end_date = (
                fields.Date.to_date(post.get("rental_end_date"))
                if post.get("rental_end_date")
                else False
            )
        except (TypeError, ValueError):
            return request.redirect("/rentals?error=dates")
        if rental_end_date and rental_end_date < rental_start_date:
            return request.redirect("/rentals?error=dates")

        request.env["techflex.rental.request"].sudo().create(
            {
                "first_name": post.get("first_name", "").strip(),
                "last_name": post.get("last_name", "").strip(),
                "company_name": post.get("company_name", "").strip(),
                "email": post.get("email", "").strip(),
                "phone": post.get("phone", "").strip(),
                "business_address": post.get("business_address", "").strip(),
                "equipment_desktops": bool(post.get("equipment_desktops")),
                "equipment_laptops": bool(post.get("equipment_laptops")),
                "equipment_tablets": bool(post.get("equipment_tablets")),
                "equipment_tvs": bool(post.get("equipment_tvs")),
                "equipment_projectors": bool(post.get("equipment_projectors")),
                "equipment_printers": bool(post.get("equipment_printers")),
                "equipment_accessories": bool(post.get("equipment_accessories")),
                "equipment_other": post.get("equipment_other", "").strip(),
                "specification_level": specification_level,
                "number_of_units": units,
                "rental_start_date": rental_start_date,
                "rental_end_date": rental_end_date,
                "rental_duration": post.get("rental_duration", "").strip(),
                "pickup_delivery": pickup_delivery,
                "additional_info": post.get("additional_info", "").strip(),
                "website_id": request.website.id,
                "submitted_from_website": True,
            }
        )
        return request.redirect("/rentals?submitted=1")

    @http.route(
        "/techflex/contact/submit",
        type="http",
        auth="public",
        methods=["POST"],
        website=True,
        csrf=True,
        sitemap=False,
    )
    def contact_submit(self, **post):
        required = ["full_name", "email", "phone", "subject", "department", "message"]
        if any(not post.get(field) for field in required):
            return request.redirect("/contact-us?error=missing")

        department = post.get("department")
        if department not in {"sales", "rentals", "orders", "support", "general"}:
            return request.redirect("/contact-us?error=department")

        request.env["techflex.contact.request"].sudo().create(
            {
                "full_name": post.get("full_name", "").strip(),
                "email": post.get("email", "").strip(),
                "phone": post.get("phone", "").strip(),
                "subject": post.get("subject", "").strip(),
                "department": department,
                "message": post.get("message", "").strip(),
                "website_id": request.website.id,
                "submitted_from_website": True,
            }
        )
        return request.redirect("/contact-us?submitted=1")
