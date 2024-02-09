# Customer Review Sentiment Analysis using Natural Language Processing

## Description:

This project scrapes reviews from consumeraffairs.com, performs sentiment analysis using VADER, stores the data in a database, exposes it through an API, and visualizes it in Power BI dashboards.

## Technologies Used:

- Python 
    - requests
    - beautifulsoup4
    - pandas
    - numpy
    - nltk
    - flask
- VADER
- MySQL
- Flask
- Power BI

## Code Structure:

``` 
│   ├── utils
│   │   ├── data
│   │   │   └── _init__.py
│   │   │   └──runscraper.py
│   │   │   └──scraper.py
│   │   ├── features
│   │   │   ├── _init__.py
│   │   │   ├── feature_engineering.py
│   │   ├── models
│   │   │   └── _init__.py
│   │   │   └──model.py
│   ├── app.py
```

## How To

1. Install required dependencies.
2. Configure database connection details.
3. Run scraping and analysis scripts.
4. Deploy the API.
5. Import Power BI dashboards and connect to the API.

## Contributing:

Pull requests and suggestions are welcome! Please refer to the contribution guidelines for more information.

