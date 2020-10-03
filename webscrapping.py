import requests
from bs4 import BeautifulSoup
import lxml


url = 'https://www1.nseindia.com/live_market/dynaContent/live_watch/option_chain/optionKeys.jsp'
headers = {'User-Agent': 'Mozilla 5.0'}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'lxml')
strikes = soup.find_all('a', href='/live_market/dynaContent/live_watch/option_chain/optionDates.jsp?symbol=NIFTY&instrument=OPTIDX&strike=9250.00')

for strike in strikes:
    print(strike.text)