from sqlalchemy import Column, String,  Float, Date

from connection import session, Base, engine
from market_client import get_nav_on_date
from consts import MF_DETAILS

class Investment(Base):
    __tablename__ = 'mutual_fund'
    date = Column(Date, primary_key=True)
    fund = Column(String(50), primary_key=True)
    nav = Column(Float)
    units = Column(Float)
    amount = Column(Float)

    def asdict(self):
        return {'date': self.date, 'fund': self.fund, 'nav': self.nav, 'units': self.units, 'amount': self.amount}

Base.metadata.create_all(engine)

def create_investment(fund_name, amount, date, nav=None, units=None):
    session.add(Investment(date=date, fund=fund_name, nav=nav, units=units, amount=amount))
    session.commit()

def get_last_investment(fund_name):
    last_investment = session.query(Investment).filter(Investment.fund == fund_name).order_by(Investment.date.desc()).first()
    return last_investment

def update_nav():
    investments = session.query(Investment).filter(Investment.nav == None)
    for investment in investments:
        nav = get_nav_on_date(MF_DETAILS[investment.fund]['CODE'], MF_DETAILS[investment.fund]['NAME'], investment.date)
        investment.units = float('%.3f' % (investment.amount/nav))
        investment.nav = float('%.3f' % nav)
    session.commit()

def get_existing_investment(date, fund):
    investment = session.query(Investment).filter(Investment.date == date).filter(Investment.fund == fund).first()
    return investment

def update_investment(investment):
    session.add(investment)
    session.commit()


def delete_previous_data():
    session.query(Investment).delete()
