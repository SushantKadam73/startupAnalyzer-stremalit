import requests

url = 'https://www.w3schools.com/python/module_requests.asp'

headers = {
    'Authorization': 'Bearer jina_73637676b2844cfaaa26f733093479fch4aqHm2Cbs2DBhuiS8oGULnnqqAA',
    'X-Retain-Images': 'none',
    'X-With-Links-Summary': 'true','X-Return-Format': 'text'
}


response = requests.get(url, headers=headers)
filee=open("jin.txt","w",encoding="utf-8")
filee.write(str(response.text))