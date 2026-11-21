import requests
import pandas as pd
import plotly.express as px
import gradio as gr

BASE = "http://127.0.0.1:4004/odata/v4/procurement"

def fetch_data(entity):
    response = requests.get(f"{BASE}/{entity}", timeout=10)
    response.raise_for_status()
    return pd.DataFrame(response.json().get("value", []))

def dashboard():
    po = fetch_data("PurchaseOrders")
    gr_data = fetch_data("GoodsReceipts")
    inv = fetch_data("Inventory")
    invoices = fetch_data("SupplierInvoices")

    # KPIs
    total_orders = len(po)

    if not po.empty:
        po["quantity"] = pd.to_numeric(po["quantity"])
        po["unitPrice"] = pd.to_numeric(po["unitPrice"])
        po["orderValue"] = po["quantity"] * po["unitPrice"]
        total_value = po["orderValue"].sum()
        total_ordered = po["quantity"].sum()
    else:
        total_value = 0
        total_ordered = 0

    total_received = (
        pd.to_numeric(gr_data["receivedQuantity"]).sum()
        if not gr_data.empty else 0
    )

    matched_invoices = (
        len(invoices[invoices["status"] == "Matched"])
        if not invoices.empty else 0
    )

    fulfillment = (
        total_received / total_ordered * 100
        if total_ordered else 0
    )

    summary = f"""
    ## Procurement Performance

    | KPI | Value |
    |---|---:|
    | Purchase Orders | {total_orders} |
    | Total Purchase Value | {total_value:,.2f} SAR |
    | Units Ordered | {total_ordered} |
    | Units Received | {total_received} |
    | Fulfillment Rate | {fulfillment:.1f}% |
    | Matched Invoices | {matched_invoices} |
    """

    # Purchase order chart
    if not po.empty:
        order_chart = px.bar(
            po,
            x="material",
            y="orderValue",
            title="Purchase Order Value by Material",
            labels={
                "material": "Material",
                "orderValue": "Value (SAR)"
            }
        )
    else:
        order_chart = px.bar(title="No Purchase Orders")

    # Inventory chart
    if not inv.empty:
        inv["quantity"] = pd.to_numeric(inv["quantity"])
        inventory_chart = px.bar(
            inv,
            x="material",
            y="quantity",
            title="Current Inventory",
            labels={
                "material": "Material",
                "quantity": "Quantity"
            }
        )
    else:
        inventory_chart = px.bar(title="No Inventory Data")

    return (
        summary,
        order_chart,
        inventory_chart,
        po,
        gr_data,
        inv,
        invoices
    )

with gr.Blocks(title="SAP Procurement Dashboard") as demo:

    gr.Markdown(
        "# SAP Procurement & Inventory Dashboard"
    )

    gr.Markdown(
        "SAP CAP | OData Services | Procurement Analytics"
    )

    refresh = gr.Button("Refresh Dashboard")

    summary = gr.Markdown()

    with gr.Row():
        orders_chart = gr.Plot()
        inventory_chart = gr.Plot()

    with gr.Tab("Purchase Orders"):
        po_table = gr.Dataframe(interactive=False)

    with gr.Tab("Goods Receipts"):
        gr_table = gr.Dataframe(interactive=False)

    with gr.Tab("Inventory"):
        inv_table = gr.Dataframe(interactive=False)

    with gr.Tab("Supplier Invoices"):
        invoice_table = gr.Dataframe(interactive=False)

    outputs = [
        summary,
        orders_chart,
        inventory_chart,
        po_table,
        gr_table,
        inv_table,
        invoice_table
    ]

    refresh.click(
        fn=dashboard,
        outputs=outputs
    )

    demo.load(
        fn=dashboard,
        outputs=outputs
    )

if __name__ == "__main__":
    demo.launch(server_name="127.0.0.1", server_port=7860)
