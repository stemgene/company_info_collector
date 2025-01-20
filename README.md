# company_info_collector

## Introduction

When searching for job opportunities, we often visit job boards like LinkedIn, Glassdoor, and Indeed. However, there are dozens of such websites, and it’s impossible to browse them all. Additionally, not all companies post their open positions on the platforms we frequent. As a result, we often visit individual company websites to check for newly released positions. If the number of these websites grows, manually opening dozens of sites daily becomes tedious. A unified platform that consolidates information from these customized sources is highly desirable. This project aims to address this need.

This project includes two main features:
1. Extract job position information from target companies using web scraping. If couldn't extract the available positions by some reasons, you can also put the company's name and link on the page just as a reminder.
2. Embed Google Maps to locate and display information about local companies.

## Installation

1. Create Virtual Environment
   
```sh
conda create --name info_collector python=3.11
conda activate info_collector
```
2. Install Dependencies
```sh
pip install -r requirements.txt
```
3. Configure MongoDB database and Environment Variables

Given the diversity of methods and parameters required to extract job data from different companies, NoSQL (MongoDB) is the best option for saving company information due to its ability to store data in JSON format.

You can use [MongoDB Atlas](https://www.mongodb.com/try), a simple and free way to access MongoDB services. After registering for an account and creating a cluster, obtain the necessary credentials.

Create a `.env` file in the project root directory and add the following content:
```sh
MONGODB_USERNAME=your_mongodb_username
MONGODB_PASSWORD=your_mongodb_password
```
4. 运行应用：
```sh
python dash_app/app.py
```

## Usage

### Extracting Job Position Information
Before adding company information, you need to determine whether it is technically feasible to extract job data from the company's website. Each company’s website has a unique structure, making this process the most challenging and requiring customization.

Due to my limited web scraping capabilities, I can currently extract data from specific types of website structures, such as static HTML, JSON files retrieved via fetch requests, and some dynamic websites.

A testing notebook for web scraping (`fetch_data/static_page_parsing.ipynb`) is provided. Only after successful testing can the method for extracting data from a specific website be categorized and the necessary parameters recorded in the database.

If job information cannot be extracted, you can still add the company’s information to the database by setting the "available" field to false. Although specific job positions will not be displayed, the company will still act as a reminder, prompting you to manually check its website daily.

### Home page: Display interested company positions
1. After starting the application, open your browser and visit http://127.0.0.1:8050.
2. Use the filter component to select the job types you are interested in.
3. View the filtered company job information and map locations.

### Inputting Company Information
To input company information, go to the `input company info` page and input the information manually.

Companies can be classified into three categories:

* Companies with Job Information: These companies have job positions that can be scraped and displayed.
* Companies without Job Information: These companies do not have job positions available for scraping but can be displayed as a reminder.
* Local Companies: These companies are local and can be displayed on the map.

There's some examples in `sample_data/company_info.json`


### Modifying Initial Map Coordinates
To modify the initial coordinates of the map, update the `src/pages/map.py` file. Locate the section where the map is initialized and change the latitude and longitude values to your desired coordinates.
```python
dbc.Row([
    dbc.Col([
        html.Div(id='company-list', className="card", style={'height': '75vh', 'overflowY': 'scroll'})
    ], width=3),
    dbc.Col([
        dl.Map(center=[42.3765, -71.2356], zoom=13, children=[ #replace the center with your location 
            dl.TileLayer(url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"),
            dl.LayerGroup(id="layer")
        ], style={'width': '100%', 'height': '75vh', 'margin': 'auto'})
    ], width=9)
], style={'width': '80%', 'margin': 'auto'})
```
In this example, the map is centered on New York City (latitude: 40.7128, longitude: -74.0060). Update these values to change the initial map coordinates.