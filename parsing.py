#!python3

import requests, bs4

search_raw = "Intel CPU Cooler"
search_prod = search_raw.replace(' ', '+')

res = requests.get(f'https://www.elara.ie/results.aspx?search={search_prod}')
html_obj =  bs4.BeautifulSoup(res.text, 'html.parser')
slc = html_obj.find("div")
#for i in slc:
#	if str(i).find("Gaming") != 1:
print(slc.text)

