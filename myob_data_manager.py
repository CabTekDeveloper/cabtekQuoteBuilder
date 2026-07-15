# File Created  : 15-07-2026
# By            : Wangchuk  
# Purpose       : Generate data (.txt) for MYOB App.

#--------------------------------------------------------------------------------------------------------------------------------------#
import csv
import random

import helper
import file_folder_paths
import quote_builder_db_manager as quote_builder_db

#--------------------------------------------------------------------------------------------------------------------------------------#
# COLUMN HEADINGS
col1_name             = "Co./Last Name"               # Client company name
col2_addr1            = "Addr 1 - Line 1"             # Client Company Name
col3_addr2            = "Addr 1 - Line 2"             # Client phone no
col4_addr3            = "Addr 1 - Line 3"             # Delivery type
col5_addr4            = "Addr 1 - Line 4"             # Delivery address
col6_date             = "Date"                        # *Default value: current date eg., '15/07/2026'
col7_po               = "Customer PO"                 # Quote no/name
col8_ship_via         = "Ship Via"                    # Shipping method
col9_deliv_status     = "Delivery Status"             # *Default value: 'A'
col10_desc            = "Description"                 # For Cash Sale - Append 'Client Email:' to email. Value will be Joinery, Benchtop, etc.
col11_acc_no          = "Account No."                 # Account no - Get it from ACCOUNT_NO dict above
col12_amount          = "Amount"                      # Amount - Total amount of section in number format 0.00
col13_memo            = "Journal Memo"                # Journal memo - Same as customer PO
col14_sales_last      = "Salesperson Last Name"       # Last name of person quoting
col15_sales_first     = "Salesperson First Name"      # First name of person quoting
col16_tax_code        = "Tax Code"                    # *Default value:'GST'
col17_tax_amt         = "Tax Amount"                  # Tax amount - 10% of amount
col18_freight_amt     = "Freight Amount"              # Freight amount - Value will be delivery Amount
col19_frt_tax_code    = "Freight Tax Code"            # *Default value:'GST'
col20_frt_tax_amt     = "Freight Tax Amount"          # Freight Tax Amount
col21_sale_status     = "Sale Status"                 # *Default value: - 'O' (Capital letter 'O', not number 0)

#--------------------------------------------------------------------------------------------------------------------------------------#
FIELD_NAMES = [
    col1_name,
    col2_addr1,
    col3_addr2,
    col4_addr3,
    col5_addr4,
    col6_date,
    col7_po,
    col8_ship_via,
    col9_deliv_status,
    col10_desc,
    col11_acc_no,
    col12_amount,
    col13_memo,
    col14_sales_last,
    col15_sales_first,
    col16_tax_code,
    col17_tax_amt,
    col18_freight_amt,
    col19_frt_tax_code,
    col20_frt_tax_amt,
    col21_sale_status
]
#--------------------------------------------------------------------------------------------------------------------------------------#
# Default column values for myob data. 
DEFAULT_COL_VALUES = {
    col6_date: helper.get_cur_datetime()['date_today'],
    col9_deliv_status: "A",
    col16_tax_code: "GST",
    col19_frt_tax_code: "GST",
    col21_sale_status: "O"  # Capital letter 'O'
}

# MYOB account nos
ACC_NO_JOINERY          = "4-1111"
ACC_NO_BENCHTOP         = "4-1119"
ACC_NO_ASSEMBLY_INSTALL = "4-1115"


#--------------------------------------------------------------------------------------------------------------------------------------#
# Returns a fresh dictionary record template populated with all heading keys.
# Uses the default value if specified, otherwise drops a clean empty string
def get_new_record_template():
    return {key: DEFAULT_COL_VALUES.get(key, "") for key in FIELD_NAMES}

#--------------------------------------------------------------------------------------------------------------------------------------#

def generate_myob_data_file(quote_name):
    try:
        timestamp = helper.get_cur_datetime()['timestamp']
        folder_path = file_folder_paths.FOLDER_PATH_MYOB_DATA_FILE
        file_name = f"{quote_name}_myob_{timestamp}.txt"
        file_path = f"{folder_path}\\{file_name}"

        formatted_quote_data = format_quote_data(quote_name)

        return {
            "folder_path": folder_path,
            "file_name": file_name,
            "file_path": file_path
        }
    
    except Exception as ex:
        print(f"Error in generate_myob_data_file: {ex}")

#--------------------------------------------------------------------------------------------------------------------------------------#

def format_quote_data(quote_name):
    try:
        # 1. Fetch and validate baseline data
        quote_info = quote_builder_db.get_quote_info_by_quote_name(quote_name)
        quote_data = quote_builder_db.get_quote_data(quote_name)

        if not quote_info or not quote_data:
            return False
        
        all_sections_data = quote_data.get('all_sections_data')
        if not all_sections_data:
            return False

        sections = []
        delivery_info = {}
        
        # 2. First pass: Parse delivery and determine if an assembly section exists
        # We also keep track of raw classifications so we don't have to re-evaluate string conditions
        raw_sections = []
        has_assembly_section = False

        for value in all_sections_data.values():
            section_name = value.get('section_name', '')
            name_lower = section_name.lower()

            # Handle delivery section separately
            if "delivery" in name_lower:
                if not delivery_info:
                    delivery_cost = float(value.get('section_total_cost') or 0)
                    delivery_info = {
                        "delivery_cost": round(delivery_cost, 2),
                        "tax_amount": round(delivery_cost * 0.1, 2)
                    }
                continue

            # Classify standard sections
            is_benchtop = "benchtop" in name_lower or "stone" in name_lower
            is_assembly = "assembly" in name_lower or "install" in name_lower
            
            if is_assembly:
                has_assembly_section = True

            raw_sections.append({
                "section_name": section_name,
                "section_total_cost": value.get('section_total_cost'),
                "is_benchtop": is_benchtop,
                "is_assembly": is_assembly
            })

        # 3. Second pass: Construct final section objects with the correct account numbers
        for item in raw_sections:
            if item["is_benchtop"]:
                account_no = ACC_NO_BENCHTOP
            elif item["is_assembly"] or has_assembly_section:
                account_no = ACC_NO_ASSEMBLY_INSTALL
            else:
                account_no = ACC_NO_JOINERY

            sections.append({
                "section_name": item["section_name"],
                "section_total_cost": item["section_total_cost"],
                "account_no": account_no
            })

        return {
            "quote_info": quote_info,
            "sections": sections,
            "delivery_info": delivery_info
        }
    
    except Exception as ex:
        print(f"Error : {ex}")
        return {}

#--------------------------------------------------------------------------------------------------------------------------------------#


generate_myob_data_file("QU-7511 Mel Twidale")










# # ==============================================================================
# # TEXT FILE GENERATOR
# # ==============================================================================
# def generate_text_file(file_path, data):
#     """
#     Takes a list of dictionaries and writes them to a tab-delimited text file
#     using the layout structure dictated by the FIELD_NAMES blueprint.
#     """
#     try:
#         with open(file_path, mode="w", newline="", encoding="utf-8") as f:
#             # delimiter="\t" creates a clean, industry-standard tab-delimited file
#             # extrasaction="ignore" ensures it handles unexpected dict keys gracefully
#             writer = csv.DictWriter(f, fieldnames=FIELD_NAMES, delimiter="\t", extrasaction="ignore")
            
#             # Write the header row using the variable string values
#             writer.writeheader()
            
#             # Write the list of dictionaries
#             writer.writerows(data)
            
#         print(f"Success! File created flawlessly at: {file_path}")
#     except Exception as e:
#         print(f"An error occurred while generating the file: {e}")

# # ==============================================================================
# # GENERATE MIXED-ORDER DUMMY DATA FOR TESTING
# # ==============================================================================
# def create_dummy_data(num_rows=3):
#     dummy_list = []
    
#     companies = ["Acme Corp", "Stark Industries", "Wayne Enterprises"]
#     first_names = ["John", "Tony", "Bruce"]
#     last_names = ["Doe", "Stark", "Wayne"]
    
#     for i in range(num_rows):
#         amount = round(random.uniform(100.0, 5000.0), 2)
#         tax = round(amount * 0.10, 2)
#         freight = round(random.uniform(10.0, 150.0), 2)
        
#         # We intentionally mix up the key injection order to prove
#         # that DictWriter completely reorganizes it based on the layout blueprint.
#         row = {
#             heading_7_client_po: f"PO-2026-{1000 + i}",
#             heading_12_amount: f"{amount:.2f}",
#             heading_1_co_last_name: companies[i],
#             heading_17_tax_amount: f"{tax:.2f}",
#             heading_2_addr1_line1_client_co: f"{100 + i} Industrial Way",
#             heading_6_date_export_date: "2026-07-15",
#             heading_3_addr1_line2_client_ph: f"555-010{i}",
#             heading_4_addr1_line3_delivery_type: "Commercial Courier",
#             heading_5_addr1_line4_delivery_addr: "Dock B Loading Zone",
#             heading_8_ship_via: "Road Freight",
#             heading_9_delivery_status: "A",
#             heading_10_description: "Joinery and fitout components",
#             heading_11_account_no: f"ACC-400{i}",
#             heading_13_journal_memo: f"PO-2026-{1000 + i}",
#             heading_14_salesperson_lastname: last_names[i],
#             heading_15_salesperson_firstname: first_names[i],
#             heading_16_tax_code: "GST",
#             heading_18_freight_amount: f"{freight:.2f}",
#             heading_19_freight_tax_code: "GST",
#             heading_20_freight_tax_amount: f"{round(freight * 0.10, 2):.2f}",
#             heading_21_sale_status: "O"
#         }
#         dummy_list.append(row)
        
#     return dummy_list

# # ==============================================================================
# # EXECUTION LOOP
# # ==============================================================================
# # Generate 3 rows of messy dummy records
# records_to_export = create_dummy_data(num_rows=3)
    
#     # Save target file name
# output_filename = "client_export_data.txt"
    
#     # Fire the function
# generate_text_file(output_filename, records_to_export)