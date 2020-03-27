import requests
from bs4 import BeautifulSoup
url = "https://www.coursera.org/directory/courses?authmode=signup"
response = requests.get(url)
data = response.text
soup = BeautifulSoup(data, "html.parser")
tags = soup.find_all('a')
'''for tag in tags:
     print(tag.get('href'))'''
iterss = soup.find_all("a", {"class":"c-directory-link"})
iters_no = 0
fin = {}
st = 'http://coursera.org'
st += '{0}'
for iters in iterss:
    link = iters.get('href')
    l = (iters.text)
    link = st.format(link)
    iters_no+=1
    fin[iters_no] = [l, link]
for i in range(2, 119):
    url1 = "https://www.coursera.org/directory/courses?authmode=signup&page="+str(i)
    response = requests.get(url1)
    data = response.text
    soup = BeautifulSoup(data, "html.parser")
    iterss = soup.find_all("a", {"class":"c-directory-link"})
    for iters in iterss:
       link = (iters.get('href'))
       l = iters.text
       link = st.format(link)
       iters_no+=1
       fin[iters_no] = [l, link]
import pandas as pd
links_df = pd.DataFrame.from_dict(fin, orient = 'index', columns = ['title', 'link'])
links_df.to_csv('coursera1.csv')
