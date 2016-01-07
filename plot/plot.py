import matplotlib.pyplot as plt
import numpy as np


def load_records(cms):
    datafile = '../data/stats-%s.csv' % cms
    records = {
        "php5": [],
        "php7": [],
        "hhvm": []
    }

    with open(datafile, 'r') as f:
        lines = f.readlines()
        lines.pop(0)

        try:
            while True:
                label = lines.pop(0)
                values = lines.pop(0)

                label = label.replace(' ****', '')
                label = label.replace('**** ', '')
                label = label.split('-')

                product = label[1]
                concurrency = int(label[2].strip()[1:])

                if concurrency >= 300:
                    continue

                values = [a.strip() for a in values.split(',')]
                values = {
                    "concurrency": concurrency,
                    "response_time": int(float(values[4]) * 1000),
                    "reqs_per_sec": float(values[5]),
                }

                records[product].append(values)

        except IndexError:
            pass

    return records

all_records = {
    'typo3': load_records('typo3'),
    'wordpress': load_records('wordpress'),
    'magento': load_records('magento'),
}

for cms in all_records.keys():
    records = load_records(cms)
    fig = plt.figure()
    ax = fig.gca()

    concurrencies = [a['concurrency'] for a in records['php5']]
    resp_times_php5 = [a['response_time'] for a in records['php5']]
    resp_times_php7 = [a['response_time'] for a in records['php7']]
    resp_times_hhvm = [a['response_time'] for a in records['hhvm']]

    ax.plot(concurrencies, resp_times_php5, label='PHP 5.6')
    ax.plot(concurrencies, resp_times_php7, label='PHP 7.0')
    ax.plot(concurrencies, resp_times_hhvm, label='HHVM 3.6')
    ax.set_ylabel('Response time (ms)')
    ax.set_xlabel('Concurrency')
    ax.legend(loc=2)

    fig.savefig('response-times-%s.png' % cms)


fig = plt.figure()
ax = fig.gca()
ix = np.arange(3)
w = 0.2

php5 = [
    all_records['typo3']['php5'][4]['response_time'],
    all_records['wordpress']['php5'][4]['response_time'],
    all_records['magento']['php5'][4]['response_time'],
]
php7 = [
    all_records['typo3']['php7'][4]['response_time'],
    all_records['wordpress']['php7'][4]['response_time'],
    all_records['magento']['php7'][4]['response_time'],
]
hhvm = [
    all_records['typo3']['hhvm'][4]['response_time'],
    all_records['wordpress']['hhvm'][4]['response_time'],
    all_records['magento']['hhvm'][4]['response_time'],
]

ax.bar(ix, php5, w, color='#123456', label='PHP 5.6')
ax.bar(ix + w, php7, w, color='r', label='PHP 7.0')
ax.bar(ix + 2 * w, hhvm, w, color='g', label='HHVM 3.6')
ax.set_xlim([-w, 3])
ax.legend(loc=2)
ax.set_ylabel('Response time (ms)')
locs = ax.set_xticks(ix + 1.5 * w)
labels = ax.set_xticklabels(('TYPO3 7.6', 'Wordpress 4.4', 'Magento 1.9'))

fig.savefig('response-times.png')


fig = plt.figure()
ax = fig.gca()
ix = np.arange(3)
w = 0.2

php5 = [
    all_records['typo3']['php5'][4]['reqs_per_sec'],
    all_records['wordpress']['php5'][4]['reqs_per_sec'],
    all_records['magento']['php5'][4]['reqs_per_sec'],
]
php7 = [
    all_records['typo3']['php7'][4]['reqs_per_sec'],
    all_records['wordpress']['php7'][4]['reqs_per_sec'],
    all_records['magento']['php7'][4]['reqs_per_sec'],
]
hhvm = [
    all_records['typo3']['hhvm'][4]['reqs_per_sec'],
    all_records['wordpress']['hhvm'][4]['reqs_per_sec'],
    all_records['magento']['hhvm'][4]['reqs_per_sec'],
]

ax.bar(ix, php5, w, color='b', label='PHP 5.6')
ax.bar(ix + w, php7, w, color='r', label='PHP 7.0')
ax.bar(ix + 2*w, hhvm, w, color='g', label='HHVM 3.6')
ax.set_xlim([-w, 3])
ax.legend()
ax.set_ylabel('Requests per second')
ax.set_xticks(ix + 1.5 * w)
ax.set_xticklabels(('TYPO3 7.6', 'Wordpress 4.4', 'Magento 1.9'))

fig.savefig('req-per-sec.png')
