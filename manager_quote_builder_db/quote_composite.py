import inspect
import manager_company_info as company_info_manager

from .quotes import get_quote_id_by_quote_name, get_quote_info_by_quote_name, delete_quote_by_quote_id
from .section_names import get_section_id_by_section_name, get_section_name_by_section_name_id
from .section_image_size import get_section_image_size_info
from .quote_details import (
    insert_into_quote_details_table,
    delete_quote_detials_by_quoteId_and_sectionId,
    delete_quote_details_by_quote_id,
    get_quote_details_by_quoteId_and_sectionId,
)
from .quote_section_info import (
    check_quote_section_info_exists,
    update_quote_section_info,
    insert_into_quote_section_info_table,
    get_quote_section_info_by_quote_id,
    update_quote_section_order_no,
    get_quote_section_info_by_quoteId_and_sectionNameId,
    delete_quote_section_info_by_quote_id,
    delete_quote_section_info,
)

### --------------------------------- Other Functions -----------------------------------###

# save section data to quote_details_table and quote_section_info_table
# section_data_to_save will come from the website when users click on save while creating a quote
def save_section_data(section_data_to_save):
    try:
        # get data into different variables
        quote_id = get_quote_id_by_quote_name(section_data_to_save.pop('quote_name'))
        section_name_id = get_section_id_by_section_name(section_data_to_save.pop('section_name'))
        section_image_full_names = section_data_to_save.pop('section_image_full_names').strip()
        section_detail_rows = section_data_to_save.pop('section_detail_rows')

        # add new section or update  section in quote_section_info table
        if (check_quote_section_info_exists(quote_id,section_name_id)):
            update_quote_section_info(quote_id, section_name_id, section_image_full_names)
        else:
            insert_into_quote_section_info_table(quote_id, section_name_id, section_image_full_names)
            quote_total_sections = len(get_quote_section_info_by_quote_id(quote_id))
            update_quote_section_order_no(quote_id, section_name_id,quote_total_sections)

        # delete section detail rows before adding new rows
        delete_quote_detials_by_quoteId_and_sectionId(quote_id, section_name_id)

        for row in section_detail_rows:
            insert_into_quote_details_table(quote_id, section_name_id, row['section_sub_heading'], row['section_image_row'], row['section_text'], row['section_qty_row'], row['section_unit_cost_row'],row['section_total_cost_row'])

        return True

    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
        return False




def get_quote_data(quote_name):
    quote_data = {}

    try:
        quote_info = get_quote_info_by_quote_name(quote_name)
        quote_id = quote_info['quote_id']

        section_names =[]
        all_sections_data = {}

        GST = company_info_manager.get_company_info_by_id(quote_info['company_id'])['gst']
        total_cost_ex_gst= 0
        total_cost_inc_gst =0

        # Get section names
        quote_section_info_by_quote_id =get_quote_section_info_by_quote_id(quote_id)
        for row in quote_section_info_by_quote_id:
            section_name = get_section_name_by_section_name_id(row['section_name_id'])
            section_names.append(section_name)
            # if section_name not in section_names:
            #     section_names.append(section_name)

        # Get section_row_details of each section name
        for section_name in section_names:
            section_name_id = get_section_id_by_section_name(section_name)
            temp_data = {}
            temp_data['section_name'] = section_name
            temp_data['section_name_id'] = section_name_id
            quote_section_info_by_quoteId_and_sectionNameId = get_quote_section_info_by_quoteId_and_sectionNameId(quote_id,section_name_id)

            if quote_section_info_by_quoteId_and_sectionNameId :
                section_image_full_names = quote_section_info_by_quoteId_and_sectionNameId[0]['section_image_full_names'].strip()
                if len(section_image_full_names) > 0:
                    temp_data['section_image_full_names'] = [{ "image_full_name" : item.split(';')[0], "image_size_info": get_section_image_size_info(item.split(';')[1].split('_')[1]) } for item in  section_image_full_names.split("|")]
                else:
                    temp_data['section_image_full_names']  = []
            else:
                temp_data['section_image_full_names']  = []

            quote_details_by_quoteId_and_sectionId = get_quote_details_by_quoteId_and_sectionId(quote_id,section_name_id)

            section_detail_rows = []
            section_total_cost = 0       #Wangchuk added 15-07-2026
            for section_detial_row in quote_details_by_quoteId_and_sectionId:
                temp_row ={}
                temp_row['section_sub_heading'] = section_detial_row['section_sub_heading']
                temp_row['section_image_row'] = section_detial_row['section_image_row']
                temp_row['section_text'] = section_detial_row['section_text']
                temp_row['section_qty_row'] = section_detial_row['section_qty_row']
                temp_row['section_unit_cost_row'] = section_detial_row['section_unit_cost_row']
                temp_row['section_total_cost_row'] = section_detial_row['section_total_cost_row']
                section_detail_rows.append(temp_row)

                # Wangchuk added 15-07-2026 - add all rows total cost
                section_total_cost += section_detial_row['section_total_cost_row']

                # add all the total_costs of each row
                total_cost_ex_gst += section_detial_row['section_total_cost_row']

            # Wangchuk added 15-07-2026 - add section total cost to section info
            temp_data['section_total_cost'] = round(section_total_cost,2)

            # Add each row details
            temp_data['section_detail_rows'] = section_detail_rows

            all_sections_data[section_name] = temp_data

        total_gst = round((GST/100)*total_cost_ex_gst ,2)
        total_cost_inc_gst = total_cost_ex_gst + total_gst


        # Append data
        quote_data['quote_id'] = quote_id
        quote_data['quote_name'] = quote_name
        quote_data['total_cost_ex_gst'] = round(total_cost_ex_gst,2)
        quote_data['total_gst'] = round(total_gst, 2)
        quote_data['total_cost_inc_gst'] = round(total_cost_inc_gst, 2)
        quote_data['section_names'] = section_names
        quote_data['total_sections'] = len(section_names)
        quote_data['all_sections_data'] = all_sections_data

        return quote_data

    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
        return quote_data

# print(get_quote_data("QU-7493"))
# print(get_quote_info_by_quote_name("QU-7493"))

# print(get_quote_section_info_by_quote_id(56))

#--------------------------------------------------------------------------------------------#
# this will delete quote and all its data from different tables
def delete_quote_and_its_data(quote_id):
    try:
        delete_quote_by_quote_id(quote_id)
        delete_quote_details_by_quote_id(quote_id)
        delete_quote_section_info_by_quote_id(quote_id)
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')

# To delete the selected saved section in quote_section_info_table and its details saved in quote_details_table
def delete_seleceted_section_data(quote_id, section_id):
    try:
        delete_quote_detials_by_quoteId_and_sectionId(quote_id,section_id)
        delete_quote_section_info(quote_id,section_id)
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
#--------------------------------------------------------------------------------------------#

def copy_quote_details_to_new_quote(original_quote_data, copied_quote_id):
    try:
        copied_quote_id = int(copied_quote_id)
        all_sections_data = original_quote_data['all_sections_data']
        for key, value in all_sections_data.items():
            section_name_id = value['section_name_id']
            # section_image_full_names = "|".join(value['section_image_full_names'])
            section_image_data = value['section_image_full_names']
            if section_image_data:
                section_image_full_names = "|".join([ item['image_full_name']+';imageSizeId_'+ str(item['image_size_info']['section_image_size_id']) for item in section_image_data])
            else:
                section_image_full_names = ''
            section_detail_rows = value['section_detail_rows']
            #  insert info into quote_section_info table
            insert_into_quote_section_info_table(copied_quote_id, section_name_id, section_image_full_names)

            # isert into quote_details table
            for row in section_detail_rows:
                insert_into_quote_details_table(copied_quote_id,
                                                section_name_id,
                                                row['section_sub_heading'],
                                                row['section_image_row'],
                                                row['section_text'],
                                                row['section_qty_row'],
                                                row['section_unit_cost_row'],
                                                row['section_total_cost_row']
                                            )

    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
#--------------------------------------------------------------------------------------------#
