import frappe
from frappe.model.document import Document

class Shop(Document):
    pass


#     def on_update(self):
#         """Called when a Shop document is updated."""
#         if self.airport_name:
#             update_airport_shop_counts(self.airport_name)

#     def on_trash(self):
#         """Called when a Shop document is deleted."""
#         if self.airport_name:
#             update_airport_shop_counts(self.airport_name)

# def update_airport_shop_counts(airport_name):
#     """
#     Updates the shop counts in the Airports Doctype.
#     :param airport_name: The name of the airport to update.
#     """
#     try:
#         # Total shops for the given airport
#         total_shops = frappe.db.count('Shop', filters={'airport_name': airport_name})

#         # Occupied shops for the given airport
#         occupied_shops = frappe.db.count('Shop', filters={'airport_name': airport_name, 'status': 'Occupied'})

#         # Available shops (remaining shops that are not occupied)
#         available_shops = total_shops - occupied_shops

#         # Update the counts in the Airports Doctype
#         frappe.db.set_value('Airport', airport_name, {
#             'total_shops': total_shops,
#             'occupied_shops': occupied_shops,
#             'available_shops': available_shops
#         })

#         frappe.log_error(
#             f"Shop counts updated for Airport '{airport_name}': Total = {total_shops}, "
#             f"Occupied = {occupied_shops}, Available = {available_shops}",
#             "Airport Shop Counts"
#         )
#     except Exception as e:
#         frappe.log_error(
#             f"Error updating shop counts for Airport '{airport_name}': {str(e)}",
#             "Shop Counts Update Error"
#         )
#         raise
import frappe

def update_airport_shop_counts(doc, method):
    """
    Updates the total, available, and occupied shop counts in the linked Airports doctype.
    Triggered by events on the Shop doctype.
    """
    airport_name = doc.airport  # Get the airport linked to the shop

    if not airport_name:
        return  # Exit if no airport is linked to the shop

    # Calculate total, available, and occupied shops for the given airport
    total_shop = frappe.db.count('Shop', filters={'airport': airport_name})
    occupied_shop = frappe.db.count('Shop', filters={'airport': airport_name, 'status': 'Occupied'})
    available_shop = frappe.db.count('Shop', filters={'airport': airport_name, 'status': 'Available'})

    # Update the counts in the Airports doctype
    frappe.db.set_value('Airports', airport_name, 'total_shop', total_shop)
    frappe.db.set_value('Airports', airport_name, 'occupied_shop', occupied_shop)
    frappe.db.set_value('Airports', airport_name, 'available_shop', available_shop)

