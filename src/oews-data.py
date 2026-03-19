'''
    @purpose: to get actual numbers on certain professions from OEWS
    @output: should be a CSV file or smaller if it is too much. 
    
    1. I want state level, then MSA, non-MSA level.

    It might just be easier to get everything as an XLSX file so I don't have to iterate through all the MSA/non-MSAs...
    Yes, it is literally just easier to get the xlsx files by hand and then put them in GDrive if I want to share them...
'''


import pandas as pd
import numpy as np
from plotnine import *
import seaborn as sns
import statsmodels.api as sm
from great_tables import GT
import requests
from io import StringIO


headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.8',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Referer': 'https://download.bls.gov/pub/time.series/oe/',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Sec-GPC': '1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not:A-Brand";v="99", "Brave";v="145", "Chromium";v="145"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
}

years = [str(i) for i in range(10, 20)] #2010 to 2019
print(years)
base_url = "https://www.bls.gov/oes/special.requests/oesm{}all.zip"

for yr in years:
    url = base_url.format(yr)
    response = requests.get(url, headers = headers)
    with open(f"oews_data_20{yr}.zip", 'wb') as f:
        f.write(response.content)
    print(f"Downloaded 20{yr} data.")