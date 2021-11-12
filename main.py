import urllib.request

import pandas as pd
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from matplotlib import pyplot as plt
import mplfinance as mpf

headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"}
openHeaders = ('User-Agent', "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36")

url = "https://finance.naver.com/item/sise_day.naver?code=068270"

with urlopen(Request(url, headers=headers)) as doc:
    html = BeautifulSoup(doc, 'lxml')
    pgrr = html.find('td', class_='pgRR')
    s = str(pgrr.a['href']).split('=')
    last_page = s[-1]
df = pd.DataFrame()
opener = urllib.request.build_opener()
opener.addheaders = [openHeaders]
count = 0

for page in range(int(last_page)-10, int(last_page)+1) :
    count += 1
    print(count)
    page_url = '{}&page={}'.format(url, page)
    df = df.append(pd.read_html(opener.open(page_url), header=0)[0])

df = df.dropna()

df = df.iloc[0:30]
df = df.rename(columns=
               {'날짜':'Date',
                '시가':'Open',
                '고가':'High',
                '저가':'Low',
                '종가':'Close',
                '거래량':'Volume'})
df = df.sort_values(by='Date')
df.index = pd.to_datetime(df.Date)
df=df[['Open','High','Low','Close','Volume']]
kwargs = dict(title='Celltrion customized chart', type='candle',
              mav=(2,4,6), volume=True, ylabel='ohlc candles')

mc = mpf.make_marketcolors(up='r', down='b', inherit=True)
s = mpf.make_mpf_style(marketcolors=mc)


if __name__ == '__main__':
    mpf.plot(df, **kwargs, style=s)

