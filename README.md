# FIFA 20 players data analysis and predictions

A machine learning application to help FIFA 20 career mode players to better negotiate wages, and know what positions they can use their players besides the ones suggested by the game. This repository also contains the code for scraping the relevant data from [FIFA Index website](https://www.fifaindex.com/) and a lot of interesting players data analysis.

**Important note**: with the release of FIFA 21, some of the analysis made here is outdated. However, the models can still be used since the game basically did not change this year (again! :joy:). It is also very simple to rerun the code using the FIFA Index updated players information.

## 1 - Web Scraping

All data used in this repository was scraped from FIFA Index using [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/). The relevant files for the web scraping part of the project are:

- **scraping_functions.py**: contains the definitions of the functions used to scrape FIFA Index
- **scraping_fifaindex.ipynb**: jupyter notebook with a step by step guide on how to scrape players data from FIFA Index using Beautiful Soup and the functions defined in scraping_functions.py.

## 2 - Data Analysis and visualization

All the analysis and visualizations can be found in one file:

- **fifa_players_analysis.ipynb**: jupyter notebook containing the data analysis and visualizations of FIFA 20 players.

## 3 - Machine learning models for predicting player wages and preferred positions

The models were developed and pickled in the following file:

- **ML_model_development.ipynb**: jupyter notebook containing details about the development of the predictors. There is also one section devoted to the data preparation for the Flask API

## 4 - Deploy of the model as an API

An API endpoint that can be hosted on a local webserver can be found at the **FlaskAPI** directory. The API takes in a request with a list of a given player's attributes and returns an estimated wage and his (ordered) best positions. The API was made using the flask package for python.

## 5 - Web application for predicting players wages and positions

A web application can be found at the **Streamlit_Webapp** directory. The app provides a simple user interface for getting wage and positions predictions of a given player. The user can change the player's attributes in an interactive way and get the result by a simple click of a buttom. The web app was made using the streamlit package for python.

The web application will soon be hosted in the cloud using AWS. The link will be provided here soon.

### Code and resources used

**Anaconda version**: Anaconda3-2020.07

**Python version**: 3.7.1

**Packages**: numpy, scipy, pandas, scikit-learn, matplotlib, seaborn, xgboost, pickle, requests, flask, json, streamlit

**Resources**: All references used in this project can be found inside the jupyter notebooks as hyperlinks.

If you have any problems trying to visualize the jupyter notebooks, try copying the URL into this website: https://nbviewer.jupyter.org/.
