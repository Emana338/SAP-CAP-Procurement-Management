namespace procurement;

entity Suppliers {
    key ID : UUID;
    name : String(100);
    email : String(100);
}

entity PurchaseOrders {
    key ID : UUID;
    supplier : Association to Suppliers;
    material : String(100);
    quantity : Integer;
    unitPrice : Decimal(10,2);
    status : String(30);
}

entity GoodsReceipts {
    key ID : UUID;
    purchaseOrder : Association to PurchaseOrders;
    receivedQuantity : Integer;
    receiptDate : Date;
}
entity Inventory {
 key ID : UUID;
 material : String(100);
 quantity : Integer;
 lastUpdated : Date;
}
entity SupplierInvoices {
 key ID : UUID;
 purchaseOrder : Association to PurchaseOrders;
 invoiceNumber : String(50);
 invoiceQuantity : Integer;
 invoiceAmount : Decimal(12,2);
 status : String(30);
}
