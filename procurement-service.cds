using procurement from '../db/schema';
service ProcurementService {
 entity Suppliers as projection on procurement.Suppliers;
 entity PurchaseOrders as projection on procurement.PurchaseOrders;
 entity GoodsReceipts as projection on procurement.GoodsReceipts;
 entity Inventory as projection on procurement.Inventory;
 entity SupplierInvoices as projection on procurement.SupplierInvoices;
}
