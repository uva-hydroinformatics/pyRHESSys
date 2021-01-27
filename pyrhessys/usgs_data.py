from requests import Response, Session
import pandas as pd
from bs4 import BeautifulSoup as BS
import requests

url = "https://waterservices.usgs.gov/nwis"

def station_info(st_id):
    st_id = [str(i) for i in st_id] if isinstance(st_id, list) else [str(st_id)]
    query = {"sites": ",".join(st_id)}
    site_list = []
    output_type = [{"outputDataTypeCd": "dv"}]
    payload = {
                **query,
                "format": "rdb",
                "parameterCd": "00060",
                "siteStatus": "all",
                "hasDataTypeCd": "dv",
               }
    resp = Session().post(f"{url}/site", payload).text.split("\n")
    r_list = [txt.split("\t") for txt in resp if "#" not in txt]
    r_dict = [dict(zip(r_list[0], st)) for st in r_list[2:]]
    site_list.append(pd.DataFrame.from_dict(r_dict).dropna())
    return site_list[0]

def get_streamflow(st_id, start_date, end_date):
    payload = {
                "format": "json",
                "sites": [st_id],
                "startDT": start_date,
                "endDT": end_date,
                "parameterCd": "00060",
                "statCd": "00003",
                "siteStatus": "all",
                }
    resp = Session().post(f"{url}/dv", payload)
    time_series = resp.json()["value"]["timeSeries"]
    r_ts = {t["sourceInfo"]["siteCode"][0]["value"]: t["values"][0]["value"] for t in time_series}


    def to_df(col, dic):
        discharge = pd.DataFrame.from_records(dic, exclude=["qualifiers"], index=["dateTime"])
        discharge.index = pd.to_datetime(discharge.index)
        discharge.columns = [col]
        return discharge

    qobs = pd.concat([to_df(f"USGS-{s}", t) for s, t in r_ts.items()], axis=1)
    qobs['cms'] = qobs.astype("float64") * 0.028316846592

    r = requests.get('https://waterdata.usgs.gov/nwis/inventory/?site_no='+str(st_id)+'&agency_cd=USGS&amp;')
    soup = BS(''.join(r.text), 'html.parser')
    stationTable = soup.find_all(id="stationTable")
    convert_text = str(stationTable[0].find_all("dd")[2])
    area_square_miles = float(convert_text.split(" ")[2])
    qobs['mmd'] = qobs['cms'].astype("float64")*86400000/(area_square_miles*1609*1609)
    return qobs