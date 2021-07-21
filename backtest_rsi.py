import requests
import json
import sys, getopt
import pprint

# get data from elasticsearch server 
def get_data(inputfile, symbol):
    url = 'http://localhost:9200/fidelity28_fund/_search?pretty'
    with open(inputfile) as f:
        payload = json.load(f)
    payload_json = json.dumps(payload)
    payload_json = payload_json % symbol
    headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
    r = requests.post(url, data=payload_json, headers=headers)
    return r.text

# get the command line parameters for the trading policy and the ticker symbol
def get_opt(argv):
    inputfile = ''
    symbol = 'FDEV'
    try:
        opts, args = getopt.getopt(argv, "hi:s:")
    except getopt.GetoptError:
        print('backtest_rsi -i <inputfile> -s <symbol>')
        print('example: backtest_rsi -i backtest_rsi.json -s FDEV')

    for opt, arg in opts:
        if opt == '-h':
            print('backtest_rsi -i <inputfile>')
            print('example: backtest_rsi -i backtest_rsi.json -s FDEV')
            sys.exit(0)
        elif opt in ('-i'):
            inputfile = arg
        elif opt in ('-s'):
            symbol = arg

    if inputfile == '':
        print("No input file!")
        sys.exit(-1)

    return inputfile, symbol


# parse the response data and refine the buy/sell signal
def parse_data(resp):
    result = json.loads(resp)
    aggregations = result['aggregations']
    if aggregations and 'Backtest_RSI' in aggregations:
        Backtest_RSI = aggregations['Backtest_RSI']

    transactions = []
    hold = False
    if Backtest_RSI and 'buckets' in Backtest_RSI:
        for bucket in Backtest_RSI['buckets']:
            transaction = {}
            transaction['date'] = bucket['key_as_string']
            transaction['Daily'] = bucket['Daily']['value']
            # honor buy signal if there is no share hold
            if bucket['RSI_Type']['value'] == 1 and not hold:
                transaction['buy_or_sell'] = 'buy'
                hold = True
            # honor sell signal if there is a share hold
            elif bucket['RSI_Type']['value'] == 2 and hold:
                transaction['buy_or_sell'] = 'sell'
                hold = False
            # for other situations, just hold the action
            else:
                transaction['buy_or_sell'] = 'hold'
            transactions.append(transaction)

    return transactions


def report(transactions):
    print('Transaction Sequence')
    pp = pprint.PrettyPrinter(indent=4)
    print('-' * 80)
    pp.pprint(transactions)
    print('-' * 80)
    print()

    profit = 0.0;
    num_of_buy = 0
    num_of_sell = 0
    buy_price = 0;
    win = 0
    lose = 0
    max_buy_price = 0
    for transaction in transactions:
        if transaction['buy_or_sell'] == 'buy':
           num_of_buy += 1
           buy_price = transaction['Daily']
           profit -= transaction['Daily']
           max_buy_price = transaction['Daily'] if max_buy_price < transaction['Daily'] else max_buy_price
        elif transaction['buy_or_sell'] == 'sell' and buy_price > 0:
           profit += transaction['Daily']
           if transaction['Daily'] > buy_price:
               win += 1
           else:
               lose += 1
           buy_price = 0
           num_of_sell += 1

    if buy_price > 0:
        profit += transactions[-1]['Daily']
        if transaction['Daily'] > buy_price:
            win += 1
        else:
            lose += 1

    print('number of buy:      %8d' % (num_of_buy))
    print('number of sell:     %8d' % (num_of_sell))
    print('number of win:      %8d' % (win))
    print('number of lose:     %8d' % (lose))
    print('total profit:       %8.2f' % (profit))
    print('profit/transaction: %8.2f' % (profit/num_of_buy))
    print('maximum buy price:  %8.2f' % max_buy_price)
    print('profit percent:     %8.2f%%' % (profit*100/max_buy_price))


def main(argv):
    inputfile, symbol = get_opt(argv) 
    resp = get_data(inputfile, symbol)
    transactions = parse_data(resp)
    report(transactions)


if __name__ == '__main__':
    main(sys.argv[1:])
