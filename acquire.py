import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

def get_links():
    link_list = []
    response = requests.get('https://codeup.com/blog/', headers={'user-agent': 'Codeup DS Hopper'})
    soup = BeautifulSoup(response.text)
    articles = soup.find_all('h2', class_ = 'entry-title')
    for article in articles:
        link = article.a.attrs['href']
        link_list.append(link)
    return link_list



def get_link(article):
    link = article.a.attrs['href']
    return link




def get_blog_articles():
    filename = 'codeup_blog_articles.json'
    if os.path.isfile(filename):
        return pd.read_json(filename)
    
    else:
        article_list=[]
        response = requests.get('https://codeup.com/blog/', headers={'user-agent': 'Codeup DS Hopper'})
        soup = BeautifulSoup(response.text)
        articles = soup.find_all('h2', class_ = 'entry-title')
        for article in articles:
            title = article.text
            link = get_link(article)
            article_response = requests.get(link, headers={'user-agent': 'Codeup DS Hopper'})
            article_soup = BeautifulSoup(article_response.text)
            article_content = [p.text for p in article_soup.find_all('p')]

            article = {
                'title': title, 'article_content': article_content
            }
            article_list.append(article)
        df = pd.DataFrame(article_list)
        df.to_json('codeup_blog_articles.json')
    return df


# Great, this function is working now

# let's not forget to comment the code


def get_news_articles():
    filename = 'inshort_news_articles.json'
    if os.path.isfile(filename):
        return pd.read_csv(filename)
    else:
        base_url = 'https://inshorts.com/en/read/'
        sections = ["business","sports","technology","entertainment"]
        articles = []
        for section in sections:
            response = requests.get(base_url + section, headers={'user-agent': 'ds_student'})
            soup = BeautifulSoup(response.text)
            cards = soup.select('.news-card')
            for card in cards:
                title = card.find('span',itemprop='headline').text
                author = card.find('span', class_="author").text
                content = card.find('div', itemprop="articleBody").text
                article = ({'section': section, 
                            'title': title, 
                            'author': author, 
                            'content': content})
                articles.append(article)
        df = pd.DataFrame(articles)
        df.to_json('inshort_news_articles.json')
    return df