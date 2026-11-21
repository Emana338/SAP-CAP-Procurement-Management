"""Read-only smoke checks; requires running CAP server."""
import requests
BASE = 'http://127.0.0.1:4004/odata/v4/procurement'
for entity in ('Suppliers','PurchaseOrders','GoodsReceipts','Inventory','SupplierInvoices'):
    r = requests.get(f'{BASE}/{entity}', timeout=10)
    print(f'{entity}: HTTP {r.status_code}')
    r.raise_for_status()
    assert isinstance(r.json().get('value'), list)
print('PASS: all five OData endpoints respond with lists')
