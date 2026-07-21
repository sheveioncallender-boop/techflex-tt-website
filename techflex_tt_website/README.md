# TechFlex TT Complete Website — Odoo 19

A complete, GitHub-ready website and eCommerce module for **Odoo 19 Community and Enterprise**, built for deployment through CloudPepper.

## Technical name

`techflex_tt_website`

## Included website pages

- Branded global header, footer, search panel and responsive mobile menu
- Homepage with dynamic **Monthly Specials** populated from published Odoo products
- Rentals page with the complete legacy rental-information requirements, FAQ and backend request workflow
- About Us page with an editable **3 × 3** team-member grid
- Contact Us page with form submissions, business information and editable locations
- TechFlex styling for Odoo's native Shop and product-category routes
- TechFlex styling and extra information sections for Odoo's native single-product page

## Native Odoo functionality preserved

The module inherits Odoo's existing `website_sale` templates. It does not replace the native eCommerce controllers or data flow. Odoo continues to manage:

- Published products and product categories
- Search, filters, sorting and pagination
- Product attributes and variants
- Pricelists, taxes, currencies and live prices
- Stock status and quantity controls
- Add to Cart, Buy Now, cart and checkout
- Delivery methods, payment providers and customer portal
- Product reviews and alternative products when enabled

## Additional product fields

A **TechFlex Website** tab is added to the product template with:

- Monthly Special toggle
- Product condition
- Warranty label, duration and details
- Support and delivery notes
- Key highlights
- Structured technical specification lines

Options that affect price or inventory—such as RAM, storage, colour or condition variants—should remain native Odoo product attributes and variants.

## Backend management

A **TechFlex Website** app/menu provides access to:

- Rental Requests
- Contact Requests
- Team Members
- Locations

## Dependencies

- `website_sale`
- `mail`

Both dependencies are available in Odoo 19 Community and Enterprise. The module does not depend on an Enterprise-only application.

## GitHub and CloudPepper deployment

1. Place the entire `techflex_tt_website` folder at the root of the custom-addons GitHub repository used by CloudPepper.
2. Commit and push the folder to GitHub.
3. Deploy/pull the repository in CloudPepper.
4. Restart the Odoo service or application.
5. Enable developer mode and select **Apps → Update Apps List**.
6. Search for **TechFlex TT Complete Website** and install it.
7. Publish products and mark selected products as **Monthly Special**.
8. Edit team members and locations through the **TechFlex Website** backend menu.

## Frontend assets

The module intentionally loads its CSS and JavaScript directly from `website.layout`. This follows the stable direct-assets pattern used for prior CloudPepper website deployments and reduces dependence on frontend asset-bundle compilation.

## Recommended deployment process

Install and review the module on a staging database first. Confirm the active website, product catalog, pricelist, taxes, delivery methods and payment providers before deploying to production.
