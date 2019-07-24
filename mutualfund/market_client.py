from datetime import datetime, timedelta
import requests

from consts import DATE_FORMAT

AMFI_DATE_FORMAT = '%d-%b-%Y'

def get_nav_on_date(mf_code, mf_scheme, nav_date):
    MF_URL = 'http://portal.amfiindia.com/DownloadNAVHistoryReport_Po.aspx?mf={}&tp=1&frmdt={}&todt={}'
    NAV_DATE = datetime.strftime(nav_date, AMFI_DATE_FORMAT)
    WORKING_DAY_BEFORE_NAV_DATE = datetime.strftime(nav_date - timedelta(5), AMFI_DATE_FORMAT)
    response = requests.get(MF_URL.format(mf_code, WORKING_DAY_BEFORE_NAV_DATE, NAV_DATE))
    mf_nav_line = [line for line in reversed(response.text.split('\n')) if mf_scheme in line]
    return float(mf_nav_line[0].split(';')[4])


def get_today_index_change(index):
    INDEX_URL = 'https://appfeeds.moneycontrol.com/jsonapi/market/graph&format=&ind_id={}&range=1d&type=area'
    index_data = requests.get(INDEX_URL.format(index))
    index_values = index_data.json().get('graph').get('values')
    prev_close = float(index_data.json().get('graph').get('prev_close'))
    today_avg = _get_avg(index_values)
    percent_change = ((today_avg - prev_close) / prev_close) * 100
    return percent_change


def _get_avg(data):
    sum=0
    count=0
    for item in data[-5:]:
        sum = sum+float(item['_value'])
        count = count + 1
    return sum/count