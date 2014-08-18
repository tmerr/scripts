import csv
import matplotlib
import matplotlib.pyplot as plt
from datetime import datetime


'''Only one purpose: chart csv transaction history from citizensbank.com'''


def read_citizens_csv(fname):
    '''return a tuple: (xs, ys)'''
    rdr = csv.DictReader(open(fname).readlines())
    xs = []
    ys = []
    for i in rdr:
        splt = i['Date'].split('/')
        x = datetime(year=int(splt[2]), month=int(splt[0]), day=int(splt[1]))
        xs.append(x)
        y = float(i['Amount'])
        ys.append(y)

    xnums = matplotlib.dates.date2num(xs)

    # sort result by xs
    xs1, ys1 = zip(*sorted(zip(xnums, ys)))

    return (xs1, ys1)


def plot_balance(xs, ys):
    '''balance over time relative to start date's balance'''
    cumulation = 0
    ys1 = []
    for y in ys:
        ys1.append(cumulation + y)
        cumulation += y

    plt.plot_date(xs, ys1)
    plt.ylabel('balance')
    plt.show()


if __name__ == '__main__':
    plot_balance(*read_citizens_csv('EXPORT (2).CSV'))
