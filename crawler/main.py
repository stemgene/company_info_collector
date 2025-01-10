import requests
from bs4 import BeautifulSoup
import re
import json
from selenium import webdriver
from selectolax.parser import HTMLParser
import chompjs
import customerized_companies_parsing
from parsel import Selector
from requests_html import HTMLSession
from typing import Optional, Dict, Any


class CompanyInfoReaderFromJson:
    def __init__(self):
        self.file_path = r"../private/company_info.json"

    def read_json(self) -> Dict[str, Any]: #表示一个字典，其中键是字符串类型，值可以是任意类型。
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            return data
        except FileNotFoundError:
            print(f"File not found: {self.file_path}")
            return {}
        except json.JSONDecodeError:
            print(f"Error decoding JSON from file: {self.file_path}")
            return {}

class StaticPageParser:
    def __init__(self):
        self.driver = webdriver.Chrome()

    def check_availability(self, url: str) -> Optional[requests.Response]:
        response = requests.get(url)
        try:
            if response.status_code == 200:
                return response
        except requests.RequestException:
            print("Network is not available")
        return None
    
    def parsing_by_dynamic_session(**kwargs):
        position_list = []
        session = HTMLSession()
        response = session.get(kwargs["URL"])
        soup = BeautifulSoup(response.content, "html.parser")
        company_items = soup.find_all(
            kwargs["parameters"]["tag"], attrs=kwargs["parameters"]["attribute"]
        )
        for position in company_items:
            position_list.append(position.get_text(strip=True))
        return position_list
    
    def parsing(self) -> list:
        company_info_dict = CompanyInfoReaderFromJson().read_json()
        results = []
        for company_info in company_info_dict:
            company_name = company_info['company_name']
            company_result = {"company_name": company_name, "URL": company_info["URL"]}
            url = company_info['URL']

            # check if the response is None
            response = self.check_availability(url)
            if response is None:
                continue
            
            # check website type
            # Type 1: dynamic_HTML_session: could be get info with session
            if company_info['website_type'] == 'dynamic_HTML_session':
                company_result["position_list"] = parsing_by_dynamic_session(
                    **company_info
                )
            
            # Type 2: static_response: extract data from the response of get request
            elif company_info["website_type"] == "static_response":
                company_result["position_list"] = parsing_by_response(**company_info)
            
            # Type 3: static_HTML: data can be parse by HTML elements, e.g, tags, lists, class_name
            elif company_info["website_type"] == "static_response":
                company_result["position_list"] = parsing_by_response(**company_info)
            
            
            results.append(company_result)
        return results


