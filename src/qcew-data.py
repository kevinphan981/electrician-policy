import pandas as pd
import numpy as np
from plotnine import *
import seaborn as sns
import statsmodels.api as sm
from great_tables import GT
import requests
from io import StringIO

#helper to determine the URL

def qcew_reader(year, quarter, data_type, code):
    url = f"https://data.bls.gov/cew/data/api/{year}/{quarter}/{data_type}/{code}.csv"
    r = requests.get(url)
    r.raise_for_status()
    df = pd.read_csv(StringIO(r.text))
    return df

# we assume default is annualized, 
# we want a panel from year to year, 
# and then we want industry data of a specific 6-digit NAICS
def qcew_series(years, data_type, code):
    final = pd.DataFrame()
    for y in years:
        df = qcew_reader(y, "a", data_type, code)
        # print(y, df.shape) #check
        df["year"] = y # have to make a year var
        final = pd.concat([final, df], ignore_index= True)
    return final

def qcew_downloader(year, quarter, data_type, code):
    url = f"https://data.bls.gov/cew/data/api/{year}/{quarter}/{data_type}/{code}.csv"
    filename = "electricians-qcew.bin"

    with requests.get(url, stream = True) as r:
        r.raise_for_status()
        with open(filename, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024 * 1024):  # 1 MB
                if not chunk:
                    continue
                f.write(chunk)
                f.flush()  # make sure OS flushes to disk


## programmatic way to read in county and other fips, but already have simplemaps dictionary
# county_url = "https://data.bls.gov/cew/doc/titles/area/area_titles.csv"
# r = requests.get(county_url)
# r.raise_for_status()
# county_fips = pd.read_csv(StringIO(r.text))
# print(county_fips.tail(), '\n', county_fips.shape)


def toStringFips(fips):
    #if not equal to five, then we have to fix it by padding 0s on the left hand side...
    if len(str(fips)) != 5:
        fips = '{:05d}'.format(fips)
        print(fips)
    return str(fips)

def toFipsSeries(series):
    return series.apply(toStringFips)

county_fips = pd.read_csv("raw-data/simplemaps_uscounties_basicv1.92/uscounties.csv")
county_list = toFipsSeries(county_fips["county_fips"])
print(type(county_list))

# method to finally retrieve everything. i mean it works but how do we checkpoint
df = pd.DataFrame()
years = range(2018,2020,1)
for county in county_list:
    print("County: ", county)
    try: 
        result = qcew_series(years, "area", county) #breaks at 09110
        # print("Size of dataframe: ", result.shape)
        result = result[result["industry_code"] == "238211"] # residential electrician businesses
        # print("Observations kept: ", result.shape) #should do additional check if it actually is all electricians
        df = pd.concat([result, df], ignore_index= True)
        # print("Final dataframe shape: ", df.shape)
    except:
        continue

df.to_csv('qcew-data.csv', index = False)