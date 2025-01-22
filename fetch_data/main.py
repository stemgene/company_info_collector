import requests
from bs4 import BeautifulSoup
import re
import json
from selenium import webdriver
from selectolax.parser import HTMLParser
import chompjs
from parsel import Selector
from requests_html import HTMLSession
from typing import Optional, Dict, Any, List
from database import DatabaseManager

class Company:
    def __init__(self, 
                 id: str,
                 company_name: str, 
                 URL: str, 
                 website_type: str, 
                 parameters: Dict[str, Any],
                 is_local: bool,
                 location: list,
                 category: str,
                 available: bool) -> None:
        self.id = id,
        self.company_name = company_name
        self.URL = URL
        self.website_type = website_type
        self.parameters = parameters
        self.is_local = is_local
        self.location = location
        self.category = category
        self.available = available
    
    # Company 类定义了一个 __str__ 方法，当你使用 print(company) 或 str(company) 时，会调用这个方法并返回指定的字符串。
    def __str__(self) -> str:
        return f"Company: {self.company_name}, URL: {self.URL}, Is Local: {self.is_local}, Category: {self.category}"

class CompanyInfoReaderFromJson:
    def __init__(self):
        self.file_path = r"sample_data/company_info.json"

    def read_json(self) -> List[Any]: #表示一个字典，其中键是字符串类型，值可以是任意类型。
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            return data
        except FileNotFoundError:
            print(f"File not found: {self.file_path}")
            return []
        except json.JSONDecodeError:
            print(f"Error decoding JSON from file: {self.file_path}")
            return []
        
class CompanyInfoReaderFromMongoDB:
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.query = {} # extract all data from the database
    
    def read_data_from_db(self) -> List[Any]:
        data = self.db_manager.fetch_data(query=self.query) 
        self.db_manager.close_connection()
        return data


class StaticPageParser:
    def __init__(self):
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0"

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
        id = company_original_info['_id']
        company_name = company_original_info['company_name']
        url = company_original_info['URL']
        website_type = company_original_info['website_type']
        parameters = company_original_info['parameters']
        is_local = company_original_info['is_local']
        location = company_original_info['location']
        category = company_original_info['category']
        available = company_original_info['available']
        return Company(id, company_name, url, website_type, parameters, is_local, location, category, available)
    
    def parsing_by_staticHTML(self, company: Company) -> list:
        position_list = []
        session = HTMLSession()
        response = session.get(company.URL)
        # check if the response is None
        if response is None:
            return position_list
        soup = BeautifulSoup(response.content, "html.parser")
        company_items = soup.find_all(
            company.parameters["tag"], attrs=company.parameters["attribute"]
        )
        for position in company_items:
            position_list.append(position.get_text(strip=True))
        return position_list

    def parsing_by_response(self, company: Company) -> list:
        position_list = []
        if company.parameters["method"] == "POST":
            response = requests.post(
                company.parameters["server_url"],
                headers=company.parameters["headers"],
            )
        else:
            response = requests.get(
                company.parameters["server_url"],
                headers=company.parameters["headers"],
            )
        content = response.json()
        local_vars = {"content": content, "position_list": []}
        exec(company.parameters["script"], globals(), local_vars)
        position_list = local_vars.get("position_list", [])

        return position_list
    
    def parsing(self) -> list:
        #company_original_info_dicts = CompanyInfoReaderFromJson().read_json() # read data from json file
        company_original_info_dicts = CompanyInfoReaderFromMongoDB().read_data_from_db()
        results = []
        for company_original_info in company_original_info_dicts:
            company = self.get_company_original_info(company_original_info)
            company_result = {"company_name": company.company_name, 
                              "URL": company.URL,
                              "is_local": company.is_local,
                              "category": company.category,
                              "location": company.location,
                              "parameters": company.parameters}
            
            # check website type
            # Type 1: staticHTML: could be get info with session
            if company.website_type == 'staticHTML':
                company_result["position_list"] = self.parsing_by_staticHTML(company)
            
            # Type 2: static_response: extract data from the response of get request
            elif company.website_type == "static_response":
                company_result["position_list"] = self.parsing_by_response(company)
            
            # Type 3: static_HTML: data can be parse by HTML elements, e.g, tags, lists, class_name
            elif company.website_type == "static_xpath":
                company_result["position_list"] = self.parsing_by_xpath(company)
            
            
            results.append(company_result)
            #print(results)
        return results

if __name__ == "__main__":
    parser = StaticPageParser()
    results = parser.parsing()
    print(results)
