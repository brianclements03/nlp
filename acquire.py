# imports required for the functions
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

def get_links():
    '''
    Function that returns a list of all the blog links on the codeup.com/blog webpage
    '''
    #create an empty list
    link_list = []
    # execute a .get on the blog page and assigne to 'response' variable
    response = requests.get('https://codeup.com/blog/', headers={'user-agent': 'Codeup DS Hopper'})
    # convert response to a BeautifulSoup object and assign to 'soup' variable
    soup = BeautifulSoup(response.text)
    # find all 'h2' tags with class= defined and assign to variable 'articles'
    articles = soup.find_all('h2', class_ = 'entry-title')
    # for loop extracting every individual link in the articles variable and appending to the empty list
    for article in articles:
        # define 'link' as the articles 'href' attribute
        link = article.a.attrs['href']
        # append article to list
        link_list.append(link)
    # return the list
    return link_list



def get_link(article):
    '''
    Function to get a single blog's web link from its 'article' variable assigned in other functions
    '''
    # define the 'link' as the 'href' attribute of the article variable
    link = article.a.attrs['href']
    # return the link
    return link




def get_blog_articles(cached=False):
    '''
    Function that extracts the title, date_published, and content of every blog post on the Codeup
    blot webpage and returns them in a pandas DataFrame
    '''
    # define a file that the function can look for in case of caching
    filename = 'codeup_blog_articles.json'
    # if a cached json of this name exists, the function reads it directly
    # (unless the caching argument is turned to false)
    if cached==True:
        # checking to see that a cached file actually exists in the directory
        if os.path.isfile(filename):
            # directly read and return the json if it exists
            return pd.read_json(filename)    
        # if cached is set to true, but no file exists in the directory, return a print statement
        # to the effect, and halt the function
        else:
            return print("No cached file exists in this directory, change the 'cached' argument")
    # if the file does not exist or caching is defined as 'False', build the dataframe from 
    # web scraping of the webpage
    else:
        # create empty article list
        article_list=[]
        # request the info using .get
        response = requests.get('https://codeup.com/blog/', headers={'user-agent': 'Codeup DS Hopper'})
        # make a BS object
        soup = BeautifulSoup(response.text)
        # create an 'articles' variable on the h2 tag, class defined in the method
        articles = soup.find_all('h2', class_ = 'entry-title')
        # for loop running through every article in the articles list
        for article in articles:
            # use the get_link() function defined above to get a link for every article
            link = get_link(article)
            # .get method for every article
            article_response = requests.get(link, headers={'user-agent': 'Codeup DS Hopper'})
            # BS object for every response
            article_soup = BeautifulSoup(article_response.text)
            # define title by finding the 'h1' tag and class as defined, converted to text
            title = article_soup.find('h1',class_='entry-title').text
            # define date_published by finding the 'span' tag and class as defined, converted to text
            date_published = article_soup.find('span',class_='published').text
            # define content by finding the 'div' tag and class as defined, converted to text
            article_content = article_soup.find('div',class_='entry-content').text.strip()
            # compile the previous variables into a dictionary, assigned to 'article' variable
            article = {
                'title': title, 
                'date_published': date_published,
                'article_content': article_content
            }
            # append 'article' to the articles list
            article_list.append(article)
        # convert the resulting list to a Pandas DataFrame
        df = pd.DataFrame(article_list)
        # write the resulting DF to json format
        df.to_json('codeup_blog_articles.json')
    # return the resulting df
    return df



def get_news_articles(cached=False):
    '''
    Function that extracts the title, author, content, and date_publishedf every article in each defined 
    section of the Inshort website, and returns them in a pandas DataFrame
    '''
    # define a file that the function can look for in case of caching
    filename = 'inshort_news_articles.json'
    # if a cached json of this name exists, the function reads it directly
    # (unless the caching argument is turned to false)
    if cached == True:
        # checking to see that a cached file actually exists in the directory
        if os.path.isfile(filename):
            # directly read and return the json if it exists
            return pd.read_json(filename)
        # if cached is set to true, but no file exists in the directory, return a print statement
        # to the effect, and halt the function
        else:
            return print("No cached file exists in this directory, change the 'cached' argument")
    # if the file does not exist or caching is defined as 'False', build the dataframe from 
    # web scraping of the webpage
    else:
        # define a base url for the website
        base_url = 'https://inshorts.com/en/read/'
        # define the sections this function scrapes
        sections = ["business","sports","technology","entertainment"]
        # create empty article list
        articles = []
        # for loop running through every section in the sections list
        for section in sections:
            # .get method for every section
            response = requests.get(base_url + section, headers={'user-agent': 'ds_student'})
            # BeautifulSoup object for every response
            soup = BeautifulSoup(response.text)
            # create a card for every article in the section by searching for '.news-card'
            cards = soup.select('.news-card')
            # for loop for every card, extracting the variables I need
            for card in cards:
                # define title by finding the 'span' tag and itemprop as defined, converted to text
                title = card.find('span',itemprop='headline').text
                # define author by finding the 'span' tag and class as defined, converted to text
                author = card.find('span', class_="author").text
                # define content by finding the 'div' tag and itemprop as defined, converted to text
                content = card.find('div', itemprop="articleBody").text
                # define date published by finding the 'span' tag and clas as defined, converted to text
                # a note: there appears to be a misspelling of 'class' in the html
                # but the misspelling is across cards and so the function is working correctly
                date_published = card.find('span', clas="date").text
                # compile the previous variables into a dictionary, assigned to 'article' variable
                article = ({'section': section, 
                            'title': title, 
                            'author': author, 
                            'content': content,
                            'date_published': date_published})
                # append 'article' to the articles list
                articles.append(article)
        # convert the resulting list to a Pandas DataFrame
        df = pd.DataFrame(articles)
        # write the resulting DF to json format
        df.to_json('inshort_news_articles.json')
    # return the resulting df
    return df