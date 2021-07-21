# Backtest_RSI
Materials for the article "Wow! Backtest RSI Crossover Strategy in Elasticsearch" in Medium
(https://wtwong316.medium.com/wow-backtest-rsi-crossover-strategy-in-elasticsearch-1cdf837a72a1)

The following steps have been tested with Elasticsearch Server v7.10.1

Create an index, fidelity28_fund and the corresponding data are populated. The data for the index, fidelity28_fund, is coming from IEX (Investors Exchange) with the 28 Fidelity commission-free ETFs selected for demo purpose. The time range picked is between 2020-12-15 and 2021-05-31.

./fidelity28_index.sh

After the indices are created and the data are populated, You can try different ticker symbol such as FDEV, FMAT, FTEC, FHLC, FENY, FSTA, FDIS, FQAL, FDLO, FDMO and FUTY to backtest the RSI trading strategy. A report will be shown for the statistical data.

./backtest_rsi.sh FDEV

#Example
$ ./backtest_rsi.sh FDEV
Transaction Sequence
--------------------------------------------------------------------------------
[   {'Daily': 27.2, 'buy_or_sell': 'buy', 'date': '2021-01-29'},
    {'Daily': 28.2433, 'buy_or_sell': 'sell', 'date': '2021-02-19'},
    {'Daily': 27.03, 'buy_or_sell': 'buy', 'date': '2021-03-04'},
    {'Daily': 27.093, 'buy_or_sell': 'hold', 'date': '2021-03-05'},
    {'Daily': 26.9499, 'buy_or_sell': 'hold', 'date': '2021-03-08'},
    {'Daily': 28.005, 'buy_or_sell': 'sell', 'date': '2021-03-23'},
    {'Daily': 28.0875, 'buy_or_sell': 'hold', 'date': '2021-03-26'},
    {'Daily': 28.0803, 'buy_or_sell': 'hold', 'date': '2021-03-29'},
    {'Daily': 28.6473, 'buy_or_sell': 'hold', 'date': '2021-04-14'},
    {'Daily': 28.73, 'buy_or_sell': 'hold', 'date': '2021-04-15'},
    {'Daily': 28.9401, 'buy_or_sell': 'hold', 'date': '2021-04-16'},
    {'Daily': 28.98, 'buy_or_sell': 'hold', 'date': '2021-04-19'},
    {'Daily': 28.8358, 'buy_or_sell': 'hold', 'date': '2021-04-21'},
    {'Daily': 28.9619, 'buy_or_sell': 'hold', 'date': '2021-04-26'}]
--------------------------------------------------------------------------------

number of buy:             2
number of sell:            2
number of win:             2
number of lose:            0
total profit:           2.02
profit/transaction:     1.01
maximum buy price:     27.20
profit percent:         7.42%
