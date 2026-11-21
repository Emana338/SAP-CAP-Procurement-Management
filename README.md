# SAP CAP Procurement & Inventory Management

**Portfolio prototype by Eman Mubarak — Computer Engineering**

A standalone procurement workflow application developed with **SAP Cloud Application Programming Model (CAP)**, **SAP CDS**, **OData V4**, **SAP Fiori Elements / SAPUI5**, **SQLite**, and an optional **Gradio/Plotly analytics dashboard**.

> **Scope:** This is a custom SAP CAP prototype, **not** an SAP S/4HANA instance, SAP ERP configuration, or production SAP integration. Fiori pages are configured but were not browser-verified in the uploaded evidence; the included screenshots show CAP OData previews.

## Business workflow

![Procurement workflow](docs/diagrams/procurement-workflow.png)

1. Create a supplier and purchase order.
2. Post goods receipt (cannot exceed outstanding order quantity).
3. Automatically update inventory.
4. Post supplier invoice: validate received quantity, order unit price, and duplicate invoice number.
5. Review entities via OData, Fiori, or optional dashboard.

## Architecture

![Architecture](docs/diagrams/architecture.png)

## Project structure

```text
app/procurement/annotations.cds           Fiori UI annotations
app/procurement/webapp/                   Fiori Elements UI5 application
srv/procurement-service.cds               OData V4 service
srv/procurement-service.js                Business rules
 db/schema.cds                             Domain model
 dashboard/app.py                          Optional analytics UI
 docs/screenshots/                         Actual CAP screenshots
 docs/diagrams/                            Architecture and process charts
 docs/SAP_Project_Screenshots.pdf          Screenshot-only PDF
 tests/smoke_test.py                       Non-destructive API smoke checks
```

## Run locally

Requirements: Node.js 20+ and npm; Python 3.10+ only for the optional dashboard. Internet access is needed to load SAPUI5 from `ui5.sap.com`.

```bash
npm install
npm run deploy:sqlite
npm start
```

Open `http://localhost:4004/` for the CAP service landing page, or `http://localhost:4004/procurement/webapp/index.html` for the UI5 application. The CAP landing page's entity links are **OData preview pages**, not the custom Fiori app.

Optional analytics:

```bash
pip install -r dashboard/requirements.txt
python dashboard/app.py
```

Dashboard: `http://127.0.0.1:7860` (requires the CAP backend running on port 4004).

## OData endpoints

`/odata/v4/procurement/{Suppliers,PurchaseOrders,GoodsReceipts,Inventory,SupplierInvoices}`

## Verify

```bash
python tests/smoke_test.py
node --check srv/procurement-service.js
npx cds compile srv app --to json
```

The smoke test performs read-only GET requests. Business-rule tests should be performed on a **disposable test database**.

## Screenshots and presentation

The `docs/screenshots` directory contains actual images provided from the Colab CAP session. `docs/SAP_Project_Screenshots.pdf` collects them into a standalone PDF. **These images document OData preview and CAP service screens, not validated Fiori Elements rendering.** The diagrams are authored documentation, not product screenshots.

## Known limitations

- SQLite is for demonstration, not production deployment.
- Colab and its proxy URL are temporary and not suitable as permanent hosting.
- The invoice matching implementation is a simplified purchase-order/receipt/price check, not full SAP FI/MM three-way matching.
- Concurrency, permissions, auditing, authentication, and deployment hardening are not implemented.
- The supplied notebook includes historical experiments and execution-specific IDs; the repository contains a cleaned consolidated version, not a byte-for-byte snapshot of the running Colab filesystem.
- UI5 Fiori runtime and CAP npm installation must be verified in a working Node environment.

## Evidence

Screenshots are of a test dataset and contain synthetic/demo supplier information. No credentials or SQLite database are included.
