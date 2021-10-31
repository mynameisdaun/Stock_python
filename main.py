import pandas as pd
import ssl


ssl._create_default_https_context = ssl._create_unverified_context
df = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13')[0]
df.종목코드 = df.종목코드.map('{:06d}'.format)
df = df.sort_values(by='종목코드', ascending=False)


if __name__ == '__main__':

    print(df)