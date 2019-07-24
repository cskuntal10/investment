from interface import start_ui
from core import import_data
from investment import update_nav

# if __name__ == "__main__":
#     import_data()
#     update_nav()
#     start_ui()
#


import requests
# # response = requests.post('https://www.sbimf.com/en-us/navs')
# # print(response.text)
# # from bs4 import BeautifulSoup
# # page_content = BeautifulSoup(response.content, "html.parser")
# # tags = page_content.find('a', href=True, text='SBI Blue Chip Fund')
# # import json
# # test = json.loads(response.text)
# # test1 = json.loads(test)
# # print(test1)

# response = requests.get("https://mutual-fund-api.p.rapidapi.com/api/v1/latestNav/133857",
#   headers={
#     "X-RapidAPI-Host": "mutual-fund-api.p.rapidapi.com",
#     "X-RapidAPI-Key": "d335eced59msh8674cb8556db0dep1a9616jsn4afd92deae6b"
#   }
# )
#
# print(response)