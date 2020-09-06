# FIFA 20 players data analysis and predictions

A machine learning application to help FIFA 20 career mode players to better negotiate wages, and know what position they can use their player besides the ones suggested by the game. This repository also contains the code for scraping the relevant data from [FIFA Index website](https://www.fifaindex.com/) and a lot of interesting players data analysis.

**Important note**: with the release of FIFA 21, some of the analysis and predictions made here will soon be outdated. However, it is very simple to rerun the code once the information about players is updated on FIFA Index website.

## 1 - Web Scraping

All data used in this repository was scraped from FIFA Index using [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/). The relevant files for the web scraping part of the project are:

- **scraping_functions.py**: contains the definitions of the functions used to scrape FIFA Index
- **scraping_fifaindex.ipynb**: jupyter notebook with a step by step guide on how to scrape players data from FIFA Index using Beautiful Soup and the functions defined in scraping_functions.py.

## 2 - Data Analysis and visualization

All the analysis and visualizations can be found in one file:

- **fifa_players_analysis.ipynb**: jupyter notebook containing the data analysis and visualizations of FIFA 20 players.

## 3 - Machine learning models for predicting player wages and preferred positions

Under development...

## 4 - Deploy of the model as an user application

Under development...
