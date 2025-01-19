# company_info_collector

## Introduction

This project includes two main features:
1. Extract job position information from target companies using web scraping. If couldn't extract the available positions by some reasons, you can also put the company's name and link on the page just as a reminder.
2. Embed Google Maps to locate and display information about local companies.

## 安装和运行

1. Create Virtual Environment
   
```sh
conda create --name info_collector python=3.11
conda activate info_collector

2. Install Dependencies
```sh
pip install -r requirements.txt

3. Configure MongoDB database and Environment Variables

Based on the varisity of the methods and parameters how to extract position data from different companies, the best way to save company infomation should be the NoSQL (MongoDB) which can save data with JSON format.

There's an easy and free way to get the MongoDB survice, i.e. [MongoDB Altlas] (https://www.mongodb.com/try). After registering a MongoDB account and creating, 获得相关credentials

Create a `.env` file in the project root directory and add the following content:

MONGODB_USERNAME=your_mongodb_username
MONGODB_PASSWORD=your_mongodb_password

4. 运行应用：

python dash_app/app.py

Usage
After starting the application, open your browser and visit http://127.0.0.1:8050.
Use the filter component to select the job types you are interested in.
View the filtered company job information and map locations.

Inputting Company Information
To input company information, refer to the src/pages/company_info_input.py file. Companies can be classified into three categories:

Companies with Job Information: These companies have job positions that can be scraped and displayed.
Companies without Job Information: These companies do not have job positions available for scraping but can be displayed as a reminder.
Local Companies: These companies are local and can be displayed on the map.

There's some examples in sample_data/company_info.json


Modifying Initial Map Coordinates
To modify the initial coordinates of the map, update the MapComponent.py file. Locate the section where the map is initialized and change the latitude and longitude values to your desired coordinates.

import dash_leaflet as dl

def MapComponent():
    return dl.Map(center=[40.7128, -74.0060], zoom=10, children=[
        dl.TileLayer(),
        # Add more map layers or markers here
    ])

n this example, the map is centered on New York City (latitude: 40.7128, longitude: -74.0060). Update these values to change the initial map coordinates.