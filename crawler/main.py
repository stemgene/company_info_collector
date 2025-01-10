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
    
    def parsing(self) -> list:
        company_info_dict = CompanyInfoReaderFromJson().read_json()
        results = []
        for company_info in company_info_dict:
            company_name = company_info['company_name']
            url = company_info['URL']
            response = self.check_availability(url)

            # check if the response is None
            if response is None:
                continue
            
            # check website type
            if company_info['website_type'] == 'customerized':
                result = customerized_companies_parsing.parsing(company_info, response)
                results.append(result)


