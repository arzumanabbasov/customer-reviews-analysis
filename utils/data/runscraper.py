from .scraper import Parser


def runScraper():
    url_list = [
        'https://www.consumeraffairs.com/finance/ally_bank.html',
        'https://www.consumeraffairs.com/finance/bank_of_the_west.html',
        'https://www.consumeraffairs.com/finance/upgrade-personal-loans.html',
        'https://www.consumeraffairs.com/finance/first-tech-federal-credit-union.html',
        'https://www.consumeraffairs.com/finance/union_bank.html', ]

    headers = {
        'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
                      'Mobile/15E148'}

    parser = Parser(url_list, headers)

    parser.run()


if __name__ == '__main__':
    runScraper()
