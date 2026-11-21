using ProcurementService as service
    from '../../srv/procurement-service';

annotate service.PurchaseOrders with @(
    UI.HeaderInfo: {
        TypeName: 'Purchase Order',
        TypeNamePlural: 'Purchase Orders',
        Title: { Value: material }
    },

    UI.SelectionFields: [
        material,
        status
    ],

    UI.LineItem: [
        { Value: material, Label: 'Material' },
        { Value: quantity, Label: 'Ordered Quantity' },
        { Value: unitPrice, Label: 'Unit Price' },
        { Value: status, Label: 'Status' }
    ],

    UI.Facets: [
        {
            $Type: 'UI.ReferenceFacet',
            Label: 'Purchase Order Details',
            Target: '@UI.FieldGroup#Details'
        }
    ],

    UI.FieldGroup #Details: {
        Data: [
            { Value: material },
            { Value: quantity },
            { Value: unitPrice },
            { Value: status }
        ]
    }
);

annotate service.Suppliers with @(
    UI.HeaderInfo: {
        TypeName: 'Supplier',
        TypeNamePlural: 'Suppliers',
        Title: { Value: name }
    },

    UI.LineItem: [
        { Value: name, Label: 'Supplier Name' },
        { Value: email, Label: 'Email Address' }
    ]
);

annotate service.Inventory with @(
    UI.HeaderInfo: {
        TypeName: 'Inventory Item',
        TypeNamePlural: 'Inventory'
    },

    UI.LineItem: [
        { Value: material, Label: 'Material' },
        { Value: quantity, Label: 'Stock Quantity' },
        { Value: lastUpdated, Label: 'Last Updated' }
    ]
);

annotate service.SupplierInvoices with @(
    UI.HeaderInfo: {
        TypeName: 'Supplier Invoice',
        TypeNamePlural: 'Supplier Invoices',
        Title: { Value: invoiceNumber }
    },

    UI.LineItem: [
        { Value: invoiceNumber },
        { Value: invoiceQuantity },
        { Value: invoiceAmount },
        { Value: status }
    ]
);

annotate service.GoodsReceipts with @(
 UI.HeaderInfo: { TypeName: 'Goods Receipt', TypeNamePlural: 'Goods Receipts' },
 UI.LineItem: [ {Value: purchaseOrder_ID, Label: 'Purchase Order'}, {Value: receivedQuantity, Label: 'Received Quantity'}, {Value: receiptDate, Label: 'Receipt Date'} ]
);
