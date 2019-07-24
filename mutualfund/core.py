from datetime import datetime, timedelta
import csv

from investment import create_investment, get_last_investment, get_existing_investment, update_investment
from consts import MF_DETAILS, DATE_FORMAT
from market_client import get_nav_on_date, get_today_index_change
import investment


def get_investment_suggestions():
    suggestions = []
    for fund_name in MF_DETAILS:
        last_inv = get_last_investment(fund_name)
        yday_nav = get_nav_on_date(MF_DETAILS[fund_name]['CODE'], MF_DETAILS[fund_name]['MF_PORTAL_NAME'], datetime.now() - timedelta(1))
        nav_change_till_yday = ((yday_nav - last_inv.nav) / last_inv.nav) * 100
        index_change_today = get_today_index_change(MF_DETAILS[fund_name]['BENCHMARK'])

        # if nav_change_till_yday+index_today_change < -2:
        last_inv_dict = last_inv.asdict()
        last_inv_dict['nav_change(%)'] = float('%.2f' % nav_change_till_yday)
        last_inv_dict['yday_nav'] = yday_nav
        last_inv_dict['index_today'] = float('%.2f' % index_change_today)
        suggestions.append(last_inv_dict)
    return suggestions


def import_data():
    investment.delete_previous_data()
    csv_file_name = 'transactions.csv'
    with open(csv_file_name) as csv_file:
        csvreader = csv.DictReader(csv_file)
        for row in csvreader:
            item = dict(row)
            fund_name = item[' Name of the Fund']
            date = datetime.strptime(item['Date'], '%Y-%m-%d').date()
            prev_investment = get_existing_investment(date,fund_name)
            if prev_investment:
                prev_investment.units = prev_investment.nav + float(item[' Units'])
                prev_investment.amount = prev_investment.amount + float(item[' Amount (INR)'])
                update_investment(prev_investment)
            else:
                create_investment(fund_name, float(item[' Amount (INR)']), date, float(item[' NAV']), float(item[' Units']))


def invest(fund, amount, date=None, nav=None, units=None):
    if not date:
        date = datetime.date(datetime.now())
    create_investment(fund,amount,date,nav,units)
