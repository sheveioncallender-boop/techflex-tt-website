# Installation / Upgrade

1. Replace the existing `techflex_tt_website` folder in the custom-addons repository with this folder.
2. Commit and push the complete folder to GitHub.
3. Deploy/restart the Odoo service in CloudPepper.
4. Enable developer mode, update the Apps list, and upgrade **TechFlex TT Complete Website**.
5. Clear the website/CDN cache if enabled.
6. Open the website in a private window or perform a hard refresh (`Ctrl+F5`).

Version 19.0.1.2.0 loads new cache-busted CSS and uses Google-hosted Oswald and Poppins fonts. The browser must be allowed to load `fonts.googleapis.com` and `fonts.gstatic.com` for the exact typography. Local fallbacks are included if those domains are blocked.
