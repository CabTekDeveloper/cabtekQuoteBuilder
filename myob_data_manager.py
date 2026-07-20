# File Created  : 15-07-2026
# By            : Wangchuk  
# Purpose       : Generate data (.txt) for MYOB App.

#--------------------------------------------------------------------------------------------------------------------------------------#
import pandas as pd

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


# MYOB account nos
ACC_NO_JOINERY          = "4-1111"
ACC_NO_BENCHTOP         = "4-1119"
ACC_NO_ASSEMBLY_INSTALL = "4-1115"

# Default column values for myob data. 
DEFAULT_COL_VALUES = {
    col6_date           : helper.get_cur_datetime()['date_today'],
    col12_amount        : "0.00",
    col9_deliv_status   : "A",
    col11_acc_no        : ACC_NO_JOINERY,
    col16_tax_code      : "GST",
    col17_tax_amt       : "0.00",
    col18_freight_amt   : "0.00",
    col20_frt_tax_amt   : "0.00",
    col19_frt_tax_code  : "GST",
    col21_sale_status   : "O"  # Capital letter 'O'
}
#--------------------------------------------------------------------------------------------------------------------------------------#

def generate_myob_data_file(quote_name):
    try:
        formatted_quote_data = format_quote_data(quote_name)
        if not formatted_quote_data:
            return {}

        myob_data = build_myob_data(formatted_quote_data)
        
        if not myob_data:
            return {}
        
        file_info  = create_myob_text_file(quote_name, myob_data)

        return file_info
    
    except Exception as ex:
        print(f"Error in generate_myob_data_file: {ex}")
        return {}

#--------------------------------------------------------------------------------------------------------------------------------------#

def format_quote_data(quote_name):
    try:
        # Fetch and validate baseline data
        quote_info = quote_builder_db.get_quote_info_by_quote_name(quote_name)
        quote_data = quote_builder_db.get_quote_data(quote_name)
    
        if not quote_info or not quote_data:
            return False
        
        if 'quoted_by' not in quote_info:
            quote_info['quoted_by'] = quote_builder_db.get_user_info_by_id(quote_info['user_id'])['full_name']


        all_sections_data = quote_data.get('all_sections_data')
        if not all_sections_data:
            return False

        sections = []
        delivery_info = {}
        
        # First pass: Parse delivery and determine if an assembly section exists
        # We also keep track of raw classifications so we don't have to re-evaluate string conditions
        raw_sections = []
        has_assembly_section = False

        for section in all_sections_data.values():
            section_name = section.get('section_name', '')
            name_lower = section_name.lower()

            # Handle delivery section separately
            if "delivery" in name_lower:
                if not delivery_info:
                    delivery_cost = float(section.get('section_total_cost') or 0)
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
                "section_total_cost": section['section_total_cost'],
                "is_benchtop": is_benchtop,
                "is_assembly": is_assembly
            })

        
    
        # Second pass: Construct final section objects with the correct account numbers
        for item in raw_sections:
            if item["is_benchtop"]:
                account_no = ACC_NO_BENCHTOP
            elif item["is_assembly"] or has_assembly_section:
                account_no = ACC_NO_ASSEMBLY_INSTALL
            else:
                account_no = ACC_NO_JOINERY

            # caclulate section cost and tax amount
            section_total_cost = float(item.get('section_total_cost') or 0)

            sections.append({
                "section_name": item["section_name"],
                "section_total_cost": round(section_total_cost,2),
                "section_tax_amount" : round(section_total_cost * 0.1 , 2),
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
def build_myob_data(formatted_quote_data):
    myob_data = []
    if not formatted_quote_data:
            return {}
    
    try:
        quote_info = formatted_quote_data.get('quote_info')
        sections = formatted_quote_data.get('sections')
        delivery_info = formatted_quote_data.get('delivery_info')
        
        if quote_info and sections:
            default_record = create_new_record(quote_info=quote_info, delivery_info=delivery_info)
    
            is_trade_client = quote_info['is_trade_client'] == 'yes'

            # Add a cashsale specific record
            if not is_trade_client:
                cash_sale_default_record = default_record.copy()
                cash_sale_default_record[col10_desc] = "Client Email:" + quote_info['customer_email']
                cash_sale_default_record[col18_freight_amt] = 0
                cash_sale_default_record[col20_frt_tax_amt] = 0
                myob_data.append(cash_sale_default_record)

            # Add the section records
            for section in sections:
                section_record = default_record.copy()

                section_record[col10_desc]      = section['section_name']
                section_record[col11_acc_no]    = section['account_no']
                section_record[col12_amount]    = section['section_total_cost']
                section_record[col17_tax_amt]   = section['section_tax_amount']

                myob_data.append(section_record)

            # Add the mandatory record - This record will be added to both cash and trade clients
            required_record = default_record.copy()
            required_record[col10_desc] =  "Please pay the $0000 deposit to secure your allocated cut date. Production will begin once your deposit has been received. Please email your payment confirmation to accounts@cabtek.com.au."
            required_record[col18_freight_amt] = 0
            required_record[col20_frt_tax_amt] = 0
            myob_data.append(required_record)

        return myob_data
    
    except Exception as ex:
        print(ex)
        return []
    
#--------------------------------------------------------------------------------------------------------------------------------------#

# This will return a dict with default values, quote_info and delivery info added to it.
def create_new_record(quote_info = {},delivery_info = {}):
    # Build a dict with default values
    new_record = {key: DEFAULT_COL_VALUES.get(key, "") for key in FIELD_NAMES}

    if quote_info:
        is_trade_client = quote_info['is_trade_client'] == 'yes'
        split_name = helper.get_first_n_last_name(quote_info['quoted_by'])

        new_record[col1_name]           = quote_info['customer_company']
        new_record[col2_addr1]          = quote_info['customer_company'] if is_trade_client else quote_info['customer_name']
        new_record[col3_addr2]          = quote_info['customer_phone_no']
        new_record[col4_addr3]          = quote_info['delivery_type']
        new_record[col5_addr4]          = quote_info['delivery_info']
        new_record[col7_po]             = quote_info['quote_name']
        new_record[col8_ship_via]       = quote_info['ship_via']
        new_record[col13_memo]          = quote_info['quote_name']
        new_record[col14_sales_last]    = split_name['l_name']
        new_record[col15_sales_first]   = split_name['f_name']

        if delivery_info:
            new_record[col18_freight_amt] = delivery_info['delivery_cost']
            new_record[col20_frt_tax_amt] = delivery_info['tax_amount']

        
    return new_record
#--------------------------------------------------------------------------------------------------------------------------------------#


#--------------------------------------------------------------------------------------------------------------------------------------#

def create_myob_text_file(quote_name, myob_data):
    if not myob_data:
        return {}
    
    try:    
        timestamp = helper.get_cur_datetime()['timestamp']
        folder_path = file_folder_paths.FOLDER_PATH_MYOB_DATA_FILE
        file_name = f"{quote_name}_myob_{timestamp}.txt"
        file_path = f"{folder_path}\\{file_name}"

        # Build dataframe
        df = pd.DataFrame(myob_data)

        # Add '{}' first
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("{}\n")  # Writes {} in column 1 and moves to a new line

        # Append the data
        df.to_csv(file_path, sep="\t", index=False, mode="a")

        return {
                "folder_path": folder_path,
                "file_name": file_name,
                "file_path": file_path
            }
    
    except Exception as ex:
        print(ex)
        return {}
#--------------------------------------------------------------------------------------------------------------------------------------#

# generate_myob_data_file("test")

    
    

