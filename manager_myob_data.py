# File Created  : 15-07-2026
# By            : Wangchuk
# Purpose       : Generate data (.txt) for MYOB App.

# --------------------------------------------------------------------------------------------------------------------------------------#
import pandas as pd
import os

import helper
import file_folder_paths
import manager_quote_builder_db as quote_builder_db

#--------------------------------------------------------------------------------------------------------------------------------------#
# COLUMN HEADINGS

# Client company name
col1_name = "Co./Last Name"  

# Client Company Name (if trade client) or Customer Name
col2_addr1 = "Addr 1 - Line 1"  

# Client phone number
col3_addr2 = "Addr 1 - Line 2"  

# Delivery type
col4_addr3 = "Addr 1 - Line 3"  

# Delivery address
col5_addr4 = "Addr 1 - Line 4"  

# Current date, e.g., '21/07/2026' (Default value)
col6_date = "Date"  

# Quote number/name
col7_po = "Customer PO"  

# Shipping method
col8_ship_via = "Ship Via"  

# Delivery status (Default value: 'A')
col9_deliv_status = "Delivery Status"  

# Item or section description (For Cash Sale header: 'Client Email: <email>')
col10_desc = "Description"  

# Account number (Mapped via ACC_NO constants)
col11_acc_no = "Account No."  

# Total amount of section formatted as 2-decimal string (0.00)
col12_amount = "Amount"  

# Journal memo (Same as Customer PO)
col13_memo = "Journal Memo"  

# Last name of person quoting
col14_sales_last = "Salesperson Last Name"  

# First name of person quoting
col15_sales_first = "Salesperson First Name"  

# Tax code (Default value: 'GST')
col16_tax_code = "Tax Code"  

# Tax amount (10% of total section amount)
col17_tax_amt = "Tax Amount"  

# Freight/delivery total amount
col18_freight_amt = "Freight Amount"  

# Freight tax code (Default value: 'GST')
col19_frt_tax_code = "Freight Tax Code"  

# Freight tax amount (10% of freight amount)
col20_frt_tax_amt = "Freight Tax Amount"  

# Sale status (Default value: Capital letter 'O', not number 0)
col21_sale_status = "Sale Status"  

# --------------------------------------------------------------------------------------------------------------------------------------#
# Field name list
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
    col21_sale_status,
]
#--------------------------------------------------------------------------------------------------------------------------------------#
# MYOB account nos
ACC_NO_JOINERY = "4-1111"
ACC_NO_BENCHTOP = "4-1119"
ACC_NO_ASSEMBLY_INSTALL = "4-1115"

#--------------------------------------------------------------------------------------------------------------------------------------#
# Default column values for MYOB data.
# Note: Currency values are stored as 2-decimal strings (e.g., "0.00") rather than floats.
# Python floats auto-strip trailing zeros (0.00 -> 0.0), which causes formatting errors in MYOB.
DEFAULT_COL_VALUES = {
    col6_date: helper.get_cur_datetime()["date_today"],
    col12_amount: "0.00",
    col9_deliv_status: "A",
    col11_acc_no: ACC_NO_JOINERY,
    col16_tax_code: "GST",
    col17_tax_amt: "0.00",
    col18_freight_amt: "0.00",
    col20_frt_tax_amt: "0.00",
    col19_frt_tax_code: "GST",
    col21_sale_status: "O",  # Capital letter 'O'
}
# --------------------------------------------------------------------------------------------------------------------------------------#
# => Entry point
def generate_myob_data_file(quote_name):
    try:
        formatted_quote_data = _format_quote_data(quote_name)
        if not formatted_quote_data:
            return {}

        myob_data = _build_myob_data(formatted_quote_data)

        if not myob_data:
            return {}
    
        file_info = _create_myob_text_file(quote_name, myob_data)

        return file_info

    except Exception as ex:
        print(f"Error in generate_myob_data_file: {ex}")
        return {}

# --------------------------------------------------------------------------------------------------------------------------------------#
def _format_quote_data(quote_name):
    sections = []
    raw_sections = []
    has_assembly_section = False

    # Initialize empty delivery info with 2-decimal string defaults
    delivery_info = {"section_total_cost": "0.00", "section_tax_amount": "0.00"}

    try:
        # Fetch and validate baseline data
        quote_info = quote_builder_db.get_quote_info_by_quote_name(quote_name)
        quote_data = quote_builder_db.get_quote_data(quote_name)

        # Exit if quote data is empty
        if not quote_info or not quote_data:
            return {}

        # Check section data exists, exit if not
        all_sections_data = quote_data.get("all_sections_data")
        if not all_sections_data:
            return {}

        # Add quoted_by to quote_info
        if "quoted_by" not in quote_info:
            user_info = quote_builder_db.get_user_info_by_id(quote_info.get("user_id"))
            quote_info["quoted_by"] = user_info.get("full_name", "") if user_info else ""

        # First pass: Parse delivery and determine if an assembly section exists
        for section in all_sections_data.values():
            section_name = section.get("section_name") or ""
            name_lower = section_name.lower()
            section_total_cost = float(section.get("section_total_cost") or 0.00)
            section_tax_amount = round(section_total_cost * 0.1, 2)

            section_total_cost_formatted = f"{section_total_cost:.2f}"
            section_tax_amount_formatted = f"{section_tax_amount:.2f}"

            # Handle delivery section separately
            if "delivery" in name_lower:
                if delivery_info["section_total_cost"] == "0.00":
                    delivery_info = {
                        "section_total_cost": section_total_cost_formatted,
                        "section_tax_amount": section_tax_amount_formatted,
                    }
                continue

            # Classify sections
            is_benchtop = "benchtop" in name_lower or "stone" in name_lower
            is_assembly = "assembly" in name_lower or "install" in name_lower or "knockup" in name_lower

            if is_assembly:
                has_assembly_section = True

            raw_sections.append(
                {
                    "section_name": section_name,
                    "section_total_cost": section_total_cost_formatted,
                    "section_tax_amount": section_tax_amount_formatted,
                    "is_benchtop": is_benchtop,
                    "is_assembly": is_assembly,
                }
            )

        # Second pass: Construct final section objects with the correct account numbers
        for section in raw_sections:
            if section["is_benchtop"]:
                account_no = ACC_NO_BENCHTOP
            else:
                if section["is_assembly"] or has_assembly_section:
                    account_no = ACC_NO_ASSEMBLY_INSTALL
                else:
                    account_no = ACC_NO_JOINERY

            section["account_no"] = account_no

            # Remove fields not required
            section.pop("is_benchtop", None)
            section.pop("is_assembly", None)

            sections.append(section)

        # Return the formatted quote data
        return {
            "quote_info": quote_info,
            "sections": sections,
            "delivery_info": delivery_info,
        }

    except Exception as ex:
        print(f"Error : {ex}")
        return {}


# --------------------------------------------------------------------------------------------------------------------------------------#
def _build_myob_data(formatted_quote_data):
    myob_data = []
    if not formatted_quote_data:
        return []

    try:
        quote_info = formatted_quote_data.get("quote_info")
        sections = formatted_quote_data.get("sections")
        delivery_info = formatted_quote_data.get("delivery_info")

        if quote_info and sections:
            default_record = _create_new_record(quote_info=quote_info, delivery_info=delivery_info)
            is_trade_client = quote_info.get("is_trade_client") == "yes"

            # Add a cashsale specific record
            if not is_trade_client:
                cash_sale_default_record = default_record.copy()
                cash_sale_default_record[col10_desc] = f"Client Email: {quote_info.get('customer_email', '')}"
                myob_data.append(cash_sale_default_record)

            # Add the section records
            for section in sections:
                if float(section.get("section_total_cost",0) or 0)  > 0:
                    section_record = default_record.copy()
                    section_record[col10_desc] = section.get("section_name", "") or ""
                    section_record[col11_acc_no] = section.get("account_no", "") or ACC_NO_JOINERY
                    section_record[col12_amount] = section.get("section_total_cost", "0.00") or "0.00"
                    section_record[col17_tax_amt] = section.get("section_tax_amount", "0.00") or "0.00"

                    myob_data.append(section_record)

            # Add the mandatory record - This record will be added to both cash and trade clients
            required_record = default_record.copy()
            required_record[col10_desc] = (
                "Please pay the $0000 deposit to secure your allocated cut date. "
                "Production will begin once your deposit has been received. "
                "Please email your payment confirmation to accounts@cabtek.com.au."
            )

            # Add the record to myob_data list
            myob_data.append(required_record)

        return myob_data

    except Exception as ex:
        print(f"Error building MYOB data: {ex}")
        return []


# --------------------------------------------------------------------------------------------------------------------------------------#


# This will return a dict with default values, quote_info and delivery info added to it.
def _create_new_record(quote_info=None, delivery_info=None):
    if quote_info is None:
        quote_info = {}
    if delivery_info is None:
        delivery_info = {}

    # Build a dict with default values
    new_record = {key: DEFAULT_COL_VALUES.get(key, "") for key in FIELD_NAMES}

    if quote_info:
        is_trade_client = quote_info.get("is_trade_client") == "yes"
        split_name = helper.get_first_n_last_name(quote_info.get("quoted_by", "")) or {"f_name": "", "l_name": ""}

        customer_company = quote_info.get("customer_company", "")
        new_record[col1_name] = customer_company
        new_record[col2_addr1] = customer_company if is_trade_client else quote_info.get("customer_name", "")
        new_record[col3_addr2] = quote_info.get("customer_phone_no", "")
        new_record[col4_addr3] = quote_info.get("delivery_type", "")
        new_record[col5_addr4] = quote_info.get("delivery_info", "")
        new_record[col7_po] = quote_info.get("quote_name", "")
        new_record[col8_ship_via] = quote_info.get("ship_via", "")
        new_record[col13_memo] = quote_info.get("quote_name", "")
        
        # Safe access for name keys
        new_record[col14_sales_last] = split_name.get("l_name", "")
        new_record[col15_sales_first] = split_name.get("f_name", "")

        if delivery_info:
            new_record[col18_freight_amt] = delivery_info.get("section_total_cost", "0.00")
            new_record[col20_frt_tax_amt] = delivery_info.get("section_tax_amount", "0.00")

    return new_record


# --------------------------------------------------------------------------------------------------------------------------------------#

def _create_myob_text_file(quote_name, myob_data):
    if not myob_data:
        return {}

    try:

        folder_path = file_folder_paths.FOLDER_PATH_MYOB_DATA_FILE
        file_name = f"{quote_name}_myob.txt"
        file_path = os.path.join(folder_path, file_name)

        # FIX: Ensure destination folder exists before writing
        os.makedirs(folder_path, exist_ok=True)

        # Build dataframe
        df = pd.DataFrame(myob_data)

        # Add '{}' header line required by MYOB
        with open(file_path, "w", encoding="utf-8", newline="") as f:
            f.write("{}\n")

        # Append myob data
        df.to_csv(file_path, sep="\t", index=False, mode="a", encoding="utf-8", lineterminator="\n")

        # return file info to generate the file download process
        return {
            "folder_path": folder_path,
            "file_name": file_name,
            "file_path": file_path,
        }

    except Exception as ex:
        print(f"Error creating MYOB text file: {ex}")
        return {}


# --------------------------------------------------------------------------------------------------------------------------------------#

# generate_myob_data_file("QU-7353 - Test Import")
