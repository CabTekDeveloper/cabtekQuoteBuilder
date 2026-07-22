DELIVERY_TYPES = [
    {   
        "id":1,
        "delivery_type":"Pick up from Cabtek",
        "delivery_info" : "7:30am - 3:00pm Mon to Fri",
        "ship_via":"Pick Up"
    },
    {   
        "id":2,
        "delivery_type":"Pls call before delivery",
        "delivery_info" : "",
        "ship_via":"TJS - 6232 9133"
    },
    {
        "id":3,
        "delivery_type":"Assembly delivery",
        "delivery_info" : "",
        "ship_via":"Cabtek To deliver"
    }
]


#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

def get_all_delivery_types():
    try:
        return DELIVERY_TYPES
    except:
        return []
# print(get_all_delivery_options())
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#