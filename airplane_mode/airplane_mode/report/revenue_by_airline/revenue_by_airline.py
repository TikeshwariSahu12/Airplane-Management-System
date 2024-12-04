# Copyright (c) 2024, Tikeshwari sahu and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
	# Define the columns for the report
	columns = [
		{'fieldname': "airline", 'label': "Airline", 'fieldtype': "Link", 'options': "Airplane", 'width': "150"},
		{'fieldname': "total_revenue", 'label': "Total Revenue", 'fieldtype': "Currency", 'options': "AED", 'width': "150"}
	]

	# Fetch all airlines
	airlines = frappe.get_all("Airline", fields=["name"])
	
	# Fetch the total revenue grouped by airline
	revenue_data = frappe.db.sql("""
		SELECT 
			airplane.airline AS airline, 
			SUM(airplane_ticket.total_amount) AS total_revenue
		FROM `tabAirplane Ticket` AS airplane_ticket
		JOIN `tabAirplane` AS airplane ON airplane.name = airplane_ticket.airplane
		WHERE airplane_ticket.docstatus = 1
		GROUP BY airplane.airline
	""", as_dict=True)
	
	# Convert to dictionary for easier lookup
	revenue_dict = {row["airline"]: row["total_revenue"] for row in revenue_data}

	# Prepare the final data by including airlines with 0 revenue
	data = []
	total_revenue = 0
	for airline in airlines:
		revenue = revenue_dict.get(airline.name, 0)
		data.append({"airline": airline.name, "total_revenue": revenue})
		total_revenue += revenue

	# Add total row
	data.append({"airline": "Total", "total_revenue": total_revenue})

	# Prepare the chart data
	chart = {
		"data": {
			"labels": [x["airline"] for x in data[:-1]],  # Exclude the total row from chart
			"datasets": [{"values": [x["total_revenue"] for x in data[:-1]]}],
		},
		"type": "donut",
	}

	# Add a summary section for total revenue
	summary = [{"label": "Total Revenue", "value": total_revenue, "datatype": "Currency"}]

	return columns, data, None, chart, summary

