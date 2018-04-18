from bs4 import BeautifulSoup
import requests

url = 'https://www.billboard.com/charts/hot-100'
html = requests.get(url).text
soup = BeautifulSoup(html, 'html.parser')
container = soup.find(class_ = 'chart-data js-chart-data')
main_dis = container.find_all(class_ = 'chart-row__main-display')
billboard_dict = {}
for cell in main_dis:
    counter = 1
    number_cont = cell.find(class_='chart-row__rank')
    number = number_cont.find(class_='chart-row__current-week')
    title_cont = cell.find(class_= 'chart-row__container')
    info = title_cont.find(class_= 'chart-row__title')
    title = info.find(class_ ='chart-row__song')
    artist = info.find(class_ ='chart-row__artist')
    billboard_dict[counter] = [title.string,artist.string]
    counter += 1







#print(main_dis)
#for cell in main_dis:
#
# chart = soup.find(class_= 'chart-row_main-display')
# print(chart)
# chart_positions = chart.find(class_='chart-row_rank')
# ranks = chart_positions.find(class_='chart-row_current-week')
# chart_names = chart.find(class_='chart-row_container')
# title = chart_data.find('h2')
