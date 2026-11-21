const cds = require('@sap/cds');
const { SELECT, INSERT, UPDATE } = cds.ql;

module.exports = (srv) => {

  const { PurchaseOrders, GoodsReceipts, Inventory, SupplierInvoices } = srv.entities;

  srv.on('CREATE', 'GoodsReceipts', async (req, next) => {

    const { purchaseOrder_ID, receivedQuantity } = req.data;

    if (!purchaseOrder_ID ||
        !Number.isInteger(receivedQuantity) ||
        receivedQuantity <= 0) {
      return req.reject(400, 'Invalid receipt data');
    }

    const tx = cds.tx(req);

    const order = await tx.run(
      SELECT.one.from(PurchaseOrders)
        .where({ ID: purchaseOrder_ID })
    );

    if (!order) {
      return req.reject(404, 'Purchase order not found');
    }

    const receipts = await tx.run(
      SELECT.from(GoodsReceipts)
        .where({ purchaseOrder_ID })
    );

    const totalReceived = receipts.reduce(
      (sum, r) => sum + r.receivedQuantity, 0
    );

    if (totalReceived + receivedQuantity > order.quantity) {
      return req.reject(
        400,
        'Goods receipt exceeds ordered quantity'
      );
    }

    const result = await next();

    const existing = await tx.run(
      SELECT.one.from(Inventory)
        .where({ material: order.material })
    );

    const today = new Date().toISOString().slice(0, 10);

    if (existing) {
      await tx.run(
        UPDATE(Inventory)
          .set({
            quantity: existing.quantity + receivedQuantity,
            lastUpdated: today
          })
          .where({ ID: existing.ID })
      );
    } else {
      await tx.run(
        INSERT.into(Inventory).entries({
          ID: cds.utils.uuid(),
          material: order.material,
          quantity: receivedQuantity,
          lastUpdated: today
        })
      );
    }

    return result;
  });


  srv.before('CREATE', 'SupplierInvoices', async (req) => {
    const { purchaseOrder_ID, invoiceQuantity,
            invoiceAmount } = req.data;

    if (!purchaseOrder_ID ||
        !Number.isInteger(invoiceQuantity) ||
        invoiceQuantity <= 0 ||
        !Number.isFinite(Number(invoiceAmount)) ||
        Number(invoiceAmount) <= 0) {
      return req.reject(400, 'Invalid invoice data');
    }

    const tx = cds.tx(req);


    // Prevent duplicate supplier invoice numbers
    const duplicateInvoice = await tx.run(
      SELECT.one.from(SupplierInvoices)
        .where({ invoiceNumber: req.data.invoiceNumber })
    );

    if (duplicateInvoice) {
      return req.reject(
        409,
        'Duplicate invoice number'
      );
    }

    const order = await tx.run(
      SELECT.one.from(PurchaseOrders)
        .where({ ID: purchaseOrder_ID })
    );

    if (!order) {
      return req.reject(404, 'Purchase order not found');
    }

    const receipts = await tx.run(
      SELECT.from(GoodsReceipts)
        .where({ purchaseOrder_ID })
    );

    const received = receipts.reduce(
      (sum, r) => sum + r.receivedQuantity, 0
    );

    const invoices = await tx.run(
      SELECT.from(SupplierInvoices)
        .where({ purchaseOrder_ID, status: 'Matched' })
    );

    const alreadyInvoiced = invoices.reduce(
      (sum, i) => sum + i.invoiceQuantity, 0
    );

    if (invoiceQuantity > received - alreadyInvoiced) {
      return req.reject(
        400,
        'Invoice quantity exceeds uninvoiced received quantity'
      );
    }

    const expectedAmount =
      Math.round(invoiceQuantity * Number(order.unitPrice) * 100);

    const actualAmount =
      Math.round(Number(invoiceAmount) * 100);

    if (expectedAmount !== actualAmount) {
      return req.reject(
        400,
        'Invoice amount does not match purchase order'
      );
    }

    req.data.status = 'Matched';
  });

};
