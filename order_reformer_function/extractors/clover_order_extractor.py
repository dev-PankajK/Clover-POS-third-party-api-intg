import json
from typing import Union, List, Any
import requests

class MenuItemExtractor:
    def __init__(self, **entries):
        self.__dict__.update(entries)

    def get_quantity(self):
        isUnitPrice = "unitQty" in self.__dict__.keys()
        quantity = int(self.__dict__["unitQty"] / 1000) if isUnitPrice is True else 1
        return quantity

    # TODO: Cache modifier details to avoid too many requests error
    def get_modifier_details(self, modifications):
        modifier_details = []
        modifiers = modifications["elements"]
    #TODO: Need to optimize the code for modifiers
        for item in modifiers:
            mod_line_item_id = item["id"]
            modAmount = item["amount"]
            modID = item["modifier"]["id"]
            base_url = "https://www.clover.com/v3/merchants"
            merchant_id = "VMR1DVW4RK291"
            url = f"{base_url}/{merchant_id}/modifiers?filter=id%3D{modID}"
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer 0121b373-466f-d4e5-6eac-f442607e624a'
            }
            response = requests.request("GET", url, headers=headers)
            response_json = json.loads(response.text)
            if response.status_code != 200:
                print(response.text)
                break
            modifierdetails = response_json["elements"][0]
            modPrice = modifierdetails["price"]
            try:
                mod_quantity = int(modAmount / modPrice)
            except ZeroDivisionError as e:
                mod_quantity = 1
            quantity = mod_quantity if mod_quantity != 0 else 1
            nesting_dict = {"client_order_line_id": mod_line_item_id, "client_menu_item_id": modID,
                        "quantity": quantity, "subtract": False}
            modifier_details.append(nesting_dict)

        return modifier_details
        
class CloverOrderExtractor:
    def __init__(self, config: dict):
        self.__dict__.update(config)

    def get_transformed_orders(self, orders: list) -> dict:
        status = self.__dict__["order_status"]
        for order in orders:
            posted_date_time = order["createdTime"]/1000
            order_id = order["id"]
            order_lines = order["lineItems"]["elements"]
            last_modified_date_time = order["modifiedTime"]/1000
            total = order["total"]/100
            data_to_send = {
                "customer_id": 45,
                "currency": 14,
                "status": status,
                "total": total,
                "order_number": order_id,
                "posted_date_time": posted_date_time,
                "last_modified_date_time": last_modified_date_time
            }
            order_item_list = []
            order_line_dict = {"order_lines": order_item_list}

            for order_line in order_lines:
                order_line_id = order_line["id"]
                try:
                    menu_item_id = order_line["item"]["id"]
                except KeyError:
                    print(f"Menu item id not found for Order/Order Line {order_id}/{order_line_id}")
                item = MenuItemExtractor(**order_line)
                quantity = item.get_quantity()
                menu_dict = {"client_order_line_id": order_line_id, "client_menu_item_id": menu_item_id,
                    "quantity": quantity, "subtract": False}
                order_line_has_modifications = "modifications" in order_line.keys()
                if order_line_has_modifications is True:
                    modifications = order_line["modifications"]
                    modifier_details = item.get_modifier_details(modifications)
                    modifier_dict = {"order_lines": modifier_details}
                    menu_dict.update(modifier_dict)

                order_item_list.append(menu_dict)

            data_to_send.update(order_line_dict)
            print(data_to_send)
            return data_to_send


    def get_live_orders(self, obj_list) -> Union[list[Any], dict]:
        orders = []
        for order_obj in obj_list:
            if ("O:" in order_obj["objectId"]):
                order_id = order_obj["objectId"][2:]
                self.__dict__.update({"order_status": order_obj["type"]})
                orders.append(self.get_an_order(order_id))
        if len(orders) == 0:
            return orders
        orders = self.get_transformed_orders(orders)
        return orders

        
    def get_an_order(self, order_id):
        BaseUrl = self.__dict__["BaseUrl"]
        httpMethod = self.__dict__["http_method"]
        mId = self.__dict__["merchant_id"]
        access_token = self.__dict__["auth_token"]
        url = f"{BaseUrl}/{mId}/orders/{order_id}?expand=lineItems,lineItems.modifications"
        headers = {
            'Authorization': f'Bearer {access_token}' # TODO: HARDCODED TOKEN
        }
        response = requests.request(httpMethod, url, headers=headers)

        if(response.status_code != 200):
            print("get_order_status_code_clover" + str(response.status_code))
        return response.json()
