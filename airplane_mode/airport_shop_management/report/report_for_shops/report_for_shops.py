import frappe

def execute(filters=None):
    data = []
    columns = [
        {"fieldname": "airport_name", "label": "Airport", "fieldtype": "Link", "options": "Airport", "width": 200},
        {"fieldname": "total_shops", "label": "Total Shops", "fieldtype": "Int", "width": 100},
        {"fieldname": "available_shops", "label": "Available Shops", "fieldtype": "Int", "width": 100},
        {"fieldname": "occupied_shops", "label": "Occupied Shops", "fieldtype": "Int", "width": 100},
    ]

    if filters.get("airport_name"):
        airport_name = filters["airport_name"]
        total_shops = frappe.db.count("Shop", {"airport_name": airport_name})
        available_shops = frappe.db.count("Shop", {"airport_name": airport_name, "status": "Available"})
        occupied_shops = frappe.db.count("Shop", {"airport_name": airport_name, "status": "Occupied"})

        data.append({
            "airport_name": airport_name,
            "total_shops": total_shops,
            "available_shops": available_shops,
            "occupied_shops": occupied_shops,
        })

    return columns, data
