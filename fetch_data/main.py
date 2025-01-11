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

class Company:
    def __init__(self, 
                 id: int,
                 company_name: str, 
                 URL: str, 
                 website_type: str, 
                 parameters: Dict[str, Any],
                 filters: list,
                 is_local: bool,
                 position: list,
                 category: str,
                 available: bool) -> None:
        self.id = id,
        self.company_name = company_name
        self.URL = URL
        self.website_type = website_type
        self.parameters = parameters
        self.filters = filters
        self.is_local = is_local
        self.position = position
        self.category = category
        self.available = available
    
    # Company 类定义了一个 __str__ 方法，当你使用 print(company) 或 str(company) 时，会调用这个方法并返回指定的字符串。
    def __str__(self) -> str:
        return f"Company: {self.company_name}, URL: {self.URL}, Is Local: {self.is_local}, Category: {self.category}"

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
    
    def get_company_original_info(self, company_original_info: Dict[str, Any]) -> Company:
        """
        Convert a dictionary of company information to a Company instance.

        Args:
            company_original_info: A dictionary containing company information.

        Returns:
            A Company instance.
        """
        id = company_original_info['id']
        company_name = company_original_info['company_name']
        url = company_original_info['URL']
        website_type = company_original_info['website_type']
        parameters = company_original_info['parameters']
        filters = company_original_info['filters']
        is_local = company_original_info['is_local']
        position = company_original_info['position']
        category = company_original_info['category']
        available = company_original_info['available']
        return Company(id, company_name, url, website_type, parameters, filters, is_local, position, category, available)
    
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
        company_original_info_dict = CompanyInfoReaderFromJson().read_json()
        results = []
        for company_original_info in company_original_info_dict:
            company = self.get_company_original_info(company_original_info)
            company_result = {"company_name": company.company_name, "URL": company.URL}

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


