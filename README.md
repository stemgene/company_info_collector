# company_info_collector

## 简介
这个项目包含两个主要功能：
1. 通过爬虫提取一些目标公司的招聘岗位信息。
2. 通过嵌入Google Maps对本地公司进行定位和信息展示。

## 安装和运行

0. 安装mongodb

https://www.mongodb.com/try/download/community-kubernetes-operator

1. Create Virtual Environment
   
```sh
conda create --name info_collector python=3.11

2. 安装依赖：
```sh
pip install -r requirements.txt

3. 初始化数据库：

python database/init_db.py

3. 导入数据：

python database/manage_db.py

4. 运行应用：

python dash_app/app.py

## 测试

使用pytest进行测试：

pytest tests/
