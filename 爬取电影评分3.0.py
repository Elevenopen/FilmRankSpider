import requests
import csv
from lxml import html
import re

# 常量
MOVIE_URL_1 = 'https://www.themoviedb.org/movie/top-rated'
MOVIE_TOP_URL = 'https://www.themoviedb.org'
MOVIE_URL_2 = 'https://www.themoviedb.org/discover/movie/items'


def get_movie_info(movie_info_url):

    resInfo = requests.get(movie_info_url)
    movInfoDoc = html.fromstring(resInfo.text)

    movInfo_name = movInfoDoc.xpath('/html/body/div[2]/main/section/div[2]/div/div/section/div[2]/section/div[1]/h2/a/text()')
    movInfo_years = movInfoDoc.xpath('/html/body/div[2]/main/section/div[2]/div/div/section/div[2]/section/div[1]/h2/span/text()')
    movInfo_dates = movInfoDoc.xpath('/html/body/div[2]/main/section/div[2]/div/div/section/div[2]/section/div[1]/div/span[@class="release"]/text()')
    movInfo_tags = movInfoDoc.xpath('/html/body/div[2]/main/section/div[2]/div/div/section/div[2]/section/div[1]/div/span[@class="genres"]/a/text()')
    movInfo_runTimes = movInfoDoc.xpath('/html/body/div[2]/main/section/div[2]/div/div/section/div[2]/section/div[1]/div/span[@class="runtime"]/text()')
    movInfo_score = movInfoDoc.xpath('/html/body/div[2]/main/section/div[2]/div/div/section/div[2]/section/div[2]/div/div/div[1]/div/div[1]/div/div/@data-percent')
    movInfo_language = movInfoDoc.xpath('/html/body/div[2]/main/section/div[3]/div/div/div[2]/div/section/div[1]/div/section[1]/p[3]/text()')
    movInfo_directors = movInfoDoc.xpath('/html/body/div[2]/main/section/div[2]/div/div/section/div[2]/section/div[3]/ol/li[1]/p[1]/a/text()') # movInfo_director
    movInfo_author = movInfoDoc.xpath('/html/body/div[2]/main/section/div[2]/div/div/section/div[2]/section/div[3]/ol/li/p[1]/a/text()') # movInfo_author
    movInfo_actor = movInfoDoc.xpath('/html/body/div[2]/main/section/div[3]/div/div/div[1]/div/section/div/ol/li/p[1]/a/text()') # movInfo_actor
    #                                 /html/body/div[2]/main/section/div[3]/div/div/div[1]/div/section[2]/div/ol/li[1]/p[1]/a/text()
    movInfo_slogan = movInfoDoc.xpath('/html/body/div[2]/main/section/div[2]/div/div/section/div[2]/section/div[3]/h3[1][@class="tagline"]/text()')
    #                                  /html/body/div[2]/main/section/div[2]/div/div/section/div[2]/section/div[3]/div/p
    movInfo_introduction = movInfoDoc.xpath('/html/body/div[2]/main/section/div[2]/div/div/section/div[2]/section/div[3]/div/p/text()')

    year = re.findall(r'\d+', movInfo_years[0].strip())[0] if movInfo_years else ''
    date = re.findall(r'.{4}-.{2}-.{2}', movInfo_dates[0].strip()) if movInfo_dates else ''

    time_str = movInfo_runTimes[0].strip() if movInfo_runTimes else ''
    hours = re.findall(r'\d+', re.findall(r'\d+h', time_str)[0])[0] if re.findall(r'\d+h', time_str) else '0'
    minutes = re.findall(r'\d+', re.findall(r'\d+m$', time_str)[0])[0] if re.findall(r'\d+m$', time_str) else '0'
    time = int(hours)*60 + int(minutes)

    movInfo = {
        '电影名': movInfo_name[0].strip() if movInfo_name else '',
        '年份': year,
        # '年份': movInfo_years[0].strip() if movInfo_years else '',
        '上映日期': date[0] if date else '',
        # '上映日期': movInfo_dates[0].strip() if movInfo_dates else '',
        '标签': ','.join(movInfo_tags) if movInfo_tags else '',
        '片长': str(time) + 'm' if time else '',
        # '片长': movInfo_runTimes[0].strip() if movInfo_runTimes else '',
        '评分': movInfo_score[0].strip() if movInfo_score else '',
        '语言': movInfo_language[0].strip() if movInfo_language else '',
        '导演': ','.join(movInfo_directors) if movInfo_directors else '',
        '作者': ','.join(movInfo_author) if movInfo_author else '',
        '演员': ','.join(movInfo_actor) if movInfo_actor else '',
        '标语': movInfo_slogan[0].strip() if movInfo_slogan else '',
        '简介': movInfo_introduction[0].strip() if movInfo_introduction else ''
    }
    # print(movInfo)
    return movInfo


def save_all_movies(all_movies):
    with open('movies1.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['电影名', '年份', '上映日期', '标签', '片长', '评分', '语言', '导演', '作者', '演员', '标语', '简介'])
        for movie in all_movies:
            writer.writerow([movie['电影名'], movie['年份'], movie['上映日期'], movie['标签'], movie['片长'], movie['评分'], movie['语言'], movie['导演'], movie['作者'], movie['演员'], movie['标语'], movie['简介']])
        print('所有电影数据已保存到 movies.csv 文件中')

def main():
    num = 0
    all_movies = []
    for page in range(1, 6):
        # 发送请求
        if page == 1:
            response = requests.get(MOVIE_URL_1)
        else:
            response = requests.post(MOVIE_URL_2,
                                     data=f'air_date.gte=&air_date.lte=&certification=&certification_country=CN&debug=&first_air_date.gte=&first_air_date.lte=&include_adult=false&include_softcore=false&latest_ceremony.gte=&latest_ceremony.lte=&page={page}&primary_release_date.gte=&primary_release_date.lte=&region=&release_date.gte=&release_date.lte=2027-03-17&show_me=undefined&sort_by=vote_average.desc&vote_average.gte=0&vote_average.lte=10&vote_count.gte=300&watch_region=CN&with_genres=&with_keywords=&with_networks=&with_origin_country=&with_original_language=&with_watch_monetization_types=&with_watch_providers=&with_release_type=&with_runtime.gte=0&with_runtime.lte=400')
        # 解析数据,获取电影列表//*[@id="cmp-51604d3d"]/div            /html/body/div[2]/main/section/div/div/div/div[2]/div[2]/div/section/div/div/div[1]/div/div[1]
        movie_list = html.fromstring(response.text).xpath(
            '//*[@class="media-card-list contents w-full"]/div/div')  # /html/body/div[2]/main/section/div/div/div/div[2]/div[2]/div/section/div/div/div[1]/div/div')
        for movie in movie_list:
            movie_urls = movie.xpath('./div/div/a/@href')
            if movie_urls:
                movie_info_url = MOVIE_TOP_URL + movie_urls[0]
                # print(movie_info_url)
                # 遍历电影列表,获取电影详细数据
                movie_info = get_movie_info(movie_info_url)
                all_movies.append(movie_info)
                print('正在获取电影数据...', movie_info['电影名'], num)
                num += 1
    # print(all_movies)

    save_all_movies(all_movies)     # 保存数据,csv文件
if __name__ == '__main__':
    main()