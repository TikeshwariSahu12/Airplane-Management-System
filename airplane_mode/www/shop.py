import frappe

def get_context(context):
    # Fetch shops with status 'Available'
    shop_list = frappe.get_all(
        "Shop",
        filters={"status": "Available"},
        fields=["shop_number","shop_name", "tenant_name", "rent_amount", "location", "status", "airport"]
    )
    context.shop_list = shop_list
    
