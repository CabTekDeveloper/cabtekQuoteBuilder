
BANK_DETAILS = {
    
    "cabtek_bank_details"   :   {
                                    "acc_name"  : "G & J Industries" ,
                                    "bank"      : "ANZ" ,
                                    "bsb"       : "012 812" ,
                                    "acc_no"    : "466953874"  
                                } ,
    
    "diy_bank_details"      :   {
                                    "acc_name"  : "DIY Custom Kitchens Pty Ltd" ,
                                    "bank"      : "ANZ" ,
                                    "bsb"       : "012 812" ,
                                    "acc_no"    : "307327104"  
                                }
    
}

# The ids in the COMPANY_INFO list below are self assigned to uniquely indentify the record and they don't relate to any external information in any way.
# If you want to add a new company, add a new dictionary to the list below. 
#   - Make sure the id is unique.
#   - Make sure to include all the key value pairs. 
#   - Make sure the keys are spelled correctly
# Most importantly, do not change the id value once assigned and the web app is in use.
COMPANY_INFO = [
    {    
        "id"    : 1 ,
        "company_name"  : "Cab-Tek Industries" ,
        "phone_no"      : "6299 7000",
        "email_id"      : "sales@cabtek.com.au" ,
        "abn"           : "35 621 778 630" ,
        "logo_path"     : "images/logo/cabtek.jpg" ,
        "gst"           : 10.0 ,
        "conditions_of_supply"    : [
                                        "All goods remain the property of Cabtek until the final invoice is paid.",
                                        "Any amendments to jobs after commencement are at customers' cost.",
                                        "Changes to original design may incur extra charges.",
                                        "Cabtek is not responsible for incorrect measurements or information supplied by customers.",
                                        "Payment methods: Cash (subject to quote), Credit Card, EFTPOS or EFT",
                                        "Please reference either the quote number or invoice number via payment",
                                        "Credit card payments incur 1.5% surcharge ex gst. (not greater than the charge to us.)",
                                        "The purchaser must accept delivery during business hours whenever possible.",
                                        "A 50% deposit is required prior to commencement of the job and full payment is required prior to dispatch.",
                                        "Full terms and conditions will be included in the final quote contract."
                                    ] ,
        "quote_footer" :  "Custom cabinet solutions for the trade" ,
        "bank_details"  : BANK_DETAILS["cabtek_bank_details"]  
    },
   
    {
        "id"    : 2 ,
        "company_name"  : "DIY Custom Kitchens" ,
        "phone_no"      : "02 6225 4363" ,
        "email_id"      : "sales@diycustomkitchens.com.au" ,
        "abn"           : "16 156 307 540" ,
        "logo_path"     : "images/logo/diy_logo.png" ,
        "gst"           : 10.0 ,
        "conditions_of_supply"    : [
                                        "Any amendments to job after commencement are at customers cost." ,
                                        "DIY Custom Kitchens are not responsible for incorrect measurements supplied by customer." ,
                                        "Payment methods: Cash, Credit Card, EFTPOS or EFT." ,
                                        "Credit card payments incur 1.5% surcharge ex gst. (not greater than charge to us.)",
                                        "The purchaser must accept delivery during business hours whenever possible." ,
                                        "Payment of 100% is required before the order can be placed" ,
                                        "Approx 20-30 day lead time. Subject to change" ,
                                        "Full terms and conditions will be included in final quote contract" 
                                    ],
        "quote_footer" :  "" ,
        "bank_details"  : BANK_DETAILS["diy_bank_details"]  
    },
]

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
def get_company_info_by_id(company_id):
    company_info = {}
    try:
        for info in COMPANY_INFO:
            if info['id'] == company_id:
                company_info = info
                break
        return company_info
    except:
        return company_info
    
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
def get_all_company_info():
    try:
        return COMPANY_INFO
    except:
        return []
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

