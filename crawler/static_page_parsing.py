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


def check_available(url):
    response = requests.get(url)
    if response.status_code == 200:
        # # 输出页面内容
        # soup = BeautifulSoup(response.text, 'html.parser')
        # content = soup.prettify()
        # output_txt(content)
        return response
    else:
        print("Network is not available.")


def output_txt(content):
    with open("page_content.txt", "w", encoding="utf-8") as f:
        f.write(content)


def content_filters(filter_parameters, content):
    """
    这个函数比较个性化，但我试着让它适配所有的json文件，主要是完成检索嵌套dict
    比如得到的json文件是data={"position name": Data Scientist, location: {"name": "MA"}}这种嵌套式的，我想要得到data["location"]["name"]
    我的输入参数就应该是"location.name"，然后通过split(".")分解出两层分别是location和name，并检索出对应的内容
    if current_key in current_data: 使用in来判断一个var是否在dict中，只能扫描当前层，不会扫描嵌套式的dict。依靠这一点来逐层递进。但其局限性在于如果深层的内容中有外层的值，则会停止在外层
    """
    position_list = []
    for filter in filter_parameters:
        for key, values in filter.items():
            path = key.split(".")  # path = ['location', 'name']
            # 以下是根据path的深度来检索指定的内容，如path=location.name，相当于两层嵌套的dict，需要的是data["location"]["name"]
            # 实现的方法是逐层递进，先用current_data = data, 然后用第一层key，然后再将current_data = current_data["location"]，接着再用第二层的key
            for position in content:
                # print(item) # {'name': 'Sales Closer Brazil', 'department': 'Sales', 'email': 'practicum.6F.A33@comeetapply.com', 'location': {'name': 'Brazil', 'country': 'BR', 'city': 'São Paulo', 'state'
                current_data = position
                for i in range(len(path)):
                    current_key = path[i]
                    if current_key in current_data:
                        if i == len(path) - 1:
                            if current_data[current_key] in values:
                                print(position["name"])
                            else:
                                current_data = current_data[current_key]
                                continue
                    break
    # for filter in len(filter_parameters):

    # for position in company_positions:
    #     if position['location']['name'] == 'USA' or position['location']['name'] == 'Remote':
    #         print(position['name'], position['location']['name'])
    return position_list


def parsing_by_tags(**kwargs):
    response = check_available(kwargs["URL"])
    soup = BeautifulSoup(response.text, "html.parser")
    position_list = []
    company_items = soup.find_all(
        kwargs["parameters"]["tag"], attrs=kwargs["parameters"]["attribute"]
    )
    for position in company_items:
        position_list.append(position.text)
    # print("position_list = ", position_list)
    return position_list


def parsing_by_script(**kwargs):
    response = check_available(kwargs["URL"])
    html = HTMLParser(response.text)
    data = html.css("script[type='text/javascript']")
    js_objects = []
    position_list = []
    for script in data:
        try:
            script_text = script.text()
            if kwargs["parameters"]["search_key"] in script_text:
                company_positions_data = chompjs.parse_js_objects(script_text)
                for item in company_positions_data:
                    js_objects.append(item)
        except:
            pass
    company_positions = js_objects[kwargs["parameters"]["index_num"]]
    # print("company_positions: \n", company_positions[0])
    if len(kwargs["filters"]) > 0:
        position_list = content_filters(kwargs["filters"], company_positions)
    return position_list


def parsing_by_response(**kwargs):
    position_list = []
    if kwargs["parameters"]["method"] == "POST":
        data = json.dumps(kwargs["parameters"]["data_json"])
        response = requests.post(
            kwargs["parameters"]["server_url"],
            headers=kwargs["parameters"]["headers"],
            data=data,
        )
        content = response.json()
        paths = kwargs["filters"]["path"].split(".")
        for hierarchy in paths:
            content = content[hierarchy]
        for item in content:
            position_list.append(item[kwargs["filters"]["index"]])
    else:  # "GET"
        response = requests.get(
            kwargs["parameters"]["server_url"], headers=kwargs["parameters"]["headers"]
        )
        content = response.json()
        # 使用exec并传递当前命名空间
        local_vars = {"content": content, "position_list": []}
        exec(kwargs["parameters"]["script"], globals(), local_vars)
        position_list = local_vars.get("position_list", [])

    return position_list


def parsing_by_xpath(**kwargs):
    position_list = []
    response = check_available(kwargs["URL"])
    data = Selector(response.text)
    result = data.xpath(kwargs["parameters"]["xpath_query"]).extract()
    for position in result:
        position_list.append(position.strip())
    return position_list


def parsing_by_dynamic(**kwargs):
    position_list = []
    # 启动 Chrome 浏览器
    options = webdriver.EdgeOptions()
    options.use_chromium = True  # 使用 Chromium
    options.add_argument("--headless")  # 添加无头模式参数，不弹出浏览器页面
    driver = webdriver.Edge(
        options=options
    )  # if the error of Edge version, download the newest
    driver = webdriver.Chrome()
    driver.get(kwargs["URL"])
    # 等待页面加载完毕
    driver.implicitly_wait(3)  # 等待时间可根据需要调整
    # 获取页面源代码
    html = driver.page_source
    # 关闭浏览器
    driver.quit()
    # 使用 BeautifulSoup 解析 HTML
    soup = BeautifulSoup(html, "html.parser")
    # soup.find_all("span", class_='job-tile__title')
    company_items = soup.find_all(
        kwargs["parameters"]["tag"], attrs=kwargs["parameters"]["attribute"]
    )
    for position in company_items:
        position_list.append(position.get_text(strip=True))
    # print("position_list = ", position_list)
    return position_list


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


def parsing(websites):
    results = []
    for company_info in websites:
        company_name = company_info["company_name"]
        company_result = {"company_name": company_name, "URL": company_info["URL"]}
        if company_info["available"] == "True":
            # Type 0: Customerized company
            if company_info["website_type"] == "static_customerized":
                company_result[
                    "position_list"
                ] = customerized_companies_parsing.handler(**company_info)

            # Type 1 static_HTML: data can be parse by HTML elements, e.g, tags, lists, class_name
            elif company_info["website_type"] == "static_HTML":
                company_result["position_list"] = parsing_by_tags(**company_info)

            # Type 2 static_script: data is stored in the script part of HTML
            elif company_info["website_type"] == "static_script":
                company_result["position_list"] = parsing_by_script(**company_info)

            # Type 3 static_response: extract data from the response of get request
            elif company_info["website_type"] == "static_response":
                company_result["position_list"] = parsing_by_response(**company_info)

            # Type 4 static_xpath: locate data by xpath
            elif company_info["website_type"] == "static_xpath":
                company_result["position_list"] = parsing_by_xpath(**company_info)

            # Type 5: dynamic_HTML: should wait for simulating actions and wait for the response
            elif company_info["website_type"] == "dynamic_HTML":
                company_result["position_list"] = parsing_by_dynamic(**company_info)

            # Type 6: dynamic_HTML_session: could be get info with session
            elif company_info["website_type"] == "dynamic_HTML_session":
                company_result["position_list"] = parsing_by_dynamic_session(
                    **company_info
                )

            results.append(company_result)

    return results

    #     # 这里可以根据网页的 HTML 结构找到需要的内容并提取
    #     # 以下是一个示例，假设你要提取所有标题和链接
    #     #list_items = soup.find_all('li', class_='list-item job row')
    #     list_items = soup.find_all('div', class_='job-tile__header')
    #     # items =  soup.find('script', type="text/javascript").text.strip()
    #     # company_positions_data = items[items.find('COMPANY_POSITIONS_DATA = [') + len('COMPANY_POSITIONS_DATA = [')::]
    #     # company_positions_data = company_positions_data[: company_positions_data.rfind(']')]
    #     # company_positions_data = json.loads(company_positions_data)
    #     # print(type(company_positions_data))
    #     # for script_tag in items:
    #     #     if 'COMPANY_DATA' in script_tag.text:
    #     #         # 找到包含 COMPANY_DATA 的部分，并提取其中的 JSON 数据
    #     #         start_index = script_tag.text.find('COMPANY_DATA') + len('COMPANY_DATA')
    #     #         end_index = script_tag.text.find(';', start_index)
    #     #         company_data_json = script_tag.text[start_index:end_index]
    #     #         print(company_data_json)

    #     #         # 使用 json.loads() 方法将 JSON 数据解析为 Python 字典对象
    #     #         #company_data_dict = json.loads(company_data_json)

    #     #         # 在这里你可以直接使用 company_data_dict 这个 Python 字典对象
    #     #         #print(company_data_dict)
    #     #         break

    #         #if 'COMPANY_DATA' in item_component.text:

    #     #links = soup.find_all('a', class_='link')
    #     for list_item in list_items:
    #         a_tag = list_item.find('a')
    #         text_of_a_tag = a_tag.text.strip()
    #         print(text_of_a_tag)

    #     # 打印标题和链接
    #     # for title, link in zip(titles, links):
    #     #     print(title.text)
    #     #     print(link['href'])

    # else:
    #     print("Failed to retrieve webpage")


# 调用函数并传入目标网站的 URL
# scrape_website('https://www.comeet.com/jobs/tripleten/98.008')
# scrape_website("https://netscoutrccorp.peoplefluent.com/res_joblist.html")
# scrape_website("https://fa-evmr-saasfaprod1.fa.ocs.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1/requisitions?lastSelectedFacet=LOCATIONS&latitude=42.464161155857674&location=239+School+St%2C+Middlesex%2C+MA%2C+United+States&longitude=-71.42785067776921&mode=geolocation&radius=25&radiusUnit=MI&selectedLocationsFacet=300000000480126")

if __name__ == "__main__":
    websites = [
        {
            "company_name": "Ramboll",
            "URL": "https://www.ramboll.com/early-careers",
            "website_type": "static_response",
            "parameters": {
                "server_url": "https://www.ramboll.com/api/jobsPosts?locale=en&countries=United%20States%20of%20America&workplace=Westford&market=&careerStage=&search=&pageNumber=1",
                "headers": {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0"
                },
                "method": "GET",
                "script": "[item['title'] for item in content['jobsPosts']['data']['jobPosts']]",
                "index_num": 0,
            },
            "filters": [],
            "position": [42.564600842578116, -71.42390798443282],
            "category": "Tech",
            "available": "True",
        }
    ]
    results = parsing(websites)
    # print("Parsing results = ", results)
