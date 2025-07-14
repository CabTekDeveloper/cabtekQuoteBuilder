import pandas as pd


#--------------------------------------------------------------------------------------------#
def prepare_and_process_excel_data_using_pandas(eo_excel_file_path):
    data = []
    processed_data = {
                        'data_processed': False,
                        'message' : "Execution error in function 'prepare_and_process_excel_data_using_pandas'" ,
                        'data':data
                      }
    
    try:
        df = pd.read_excel(eo_excel_file_path)

        # check if some of the fields we know should be in the excel file do exists to make sure we are reading the right excel file, otherwise return
        if 'PurchaseOrderNumber' not in df.columns :
            processed_data['message'] = "The excel file is not the right Eze Order File. The excel file doesn't have the required column names."
            return processed_data
        
        
        # get purchase orderr no 
        purchase_order_no_text = []
        po_no = df['PurchaseOrderNumber'].dropna().head(1).values[0]
        po_no_text = f"Purchase order no: {po_no}"
        purchase_order_no_text.append(po_no_text)
        
        
        # get internal colors
        internal_colors = []
        internal_colors_and_edge = df[['IntSerialNumber', 'IntEdge']].dropna().to_dict("records")
        for item in internal_colors_and_edge:
            color = f"{item['IntSerialNumber']} board internals, with {item['IntEdge']}"
            if color not in internal_colors:
                internal_colors.append(color)
            
            
        # get external colours
        external_colors = []
        external_colors_and_edge = df[['ExtSerialNumber', 'ExtEdge']].dropna().to_dict("records")
        for item in external_colors_and_edge:
            color = f"{item['ExtSerialNumber']} board externals, with {item['ExtEdge']}"
            if color not in external_colors:
                external_colors.append(color)
        
        
        # get finger pull
        fingerpull = []
        product_name_and_fp = df[['ProductName', 'FPDetails']].dropna().to_dict('records')
        fp_text1 = "Finger Pull drawers"
        fp_text2 = "Finger Pull doors"
        fp_text3 = "Finger Pull doors and drawers"

        for item in product_name_and_fp:
            fp = item['FPDetails'].split(',')[0]
            if fp != "0":
                if 'Drawer' in  item['ProductName']:
                    fp_info = fp_text1
                else:
                    fp_info = fp_text2
                    
                if fp_info not in fingerpull:
                    fingerpull.append(fp_info)

        if fp_text1 in fingerpull and fp_text2 in fingerpull:
            fingerpull.clear()
            fingerpull.append(fp_text3)
        
  
        
        # get product notes
        product_notes = df['ProdNotes'].dropna().tolist()   
        product_notes = [x for x in product_notes if x != 'THIS ITEM HAS BEEN DELETED.' ]
        # add all texts into data
        data = purchase_order_no_text + internal_colors + external_colors + fingerpull + product_notes
        
        # Finally, update the dict to return
        processed_data['data_processed'] = True
        processed_data['message'] ='' 
        processed_data['data'] = data
        
        return processed_data
    
    except:
        return processed_data
    



#--------------------------------------------------------------------------------------------#

