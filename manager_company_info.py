
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
        "conditions_of_supply"  : [
                                        {
                                            "title" : "Ownership of Goods",
                                            "conditions" :[
                                                "All goods remain the property of Cab-Tek Industries until full payment of the final invoice has been received and cleared."
                                            ]
                                        },
                                        
                                        {
                                            "title" : "Amendments & Variations",
                                            "conditions" :[
                                                "Any amendments to a job after commencement will be at the customer’s cost.",
                                                "Changes to the original design or scope may incur additional charges, which will be quoted and approved prior to proceeding."
                                            ]
                                        },
                                        
                                        {
                                            "title" : "Customer Responsibility",
                                            "conditions" :[
                                                "Cab-Tek Industries is not responsible for incorrect measurements, specifications, or information supplied by the customer."
                                            ]
                                        },
                                        
                                        {
                                            "title" : "Payment Terms",
                                            "conditions" :[
                                               "A 50% deposit is required within 48 hours of receiving the order confirmation.",
                                               "The final balance must be paid in full prior to the completion of production.",
                                               "Accepted payment methods: Cash, Credit Card, EFTPOS, or EFT.",
                                               "Customers should reference their invoice number when making payment.",
                                               "Mastercard and Visa payments incur a surcharge of 1.5% (exclusive of GST)",
                                               "American Express payments incur a surcharge of 2.5% (exclusive of GST)"
                                            ]
                                        },
                                        
                                        {
                                            "title" : "Delivery & Risk",
                                            "conditions" :[
                                               "The purchaser must accept delivery during standard business hours whenever reasonably possible.",
                                               "Risk in the goods passes to the purchaser upon delivery, regardless of whether full payment has been made."
                                            ]
                                        },
                                        
                                        {
                                            "title" : "Refunds & Cancellations",
                                            "conditions" :[
                                               "Deposits are non-refundable once an order has been confirmed and production has commenced.",
                                               "Orders may only be cancelled or postponed with the written consent of Cab-Tek Industries. Any costs incurred up to the date of cancellation (including materials, labour, and administration fees) will be charged to the customer.",
                                               "Custom-made, special-order, or modified goods cannot be returned or refunded unless required under the Australian Consumer Law."
                                            ]
                                        }
                                        
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

