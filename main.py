import matplotlib.pyplot as plt
import array as arr
import numpy as np

name = []
deaths = []
dx = 2000


def plot_4_scales_hist(counts, bins, title, fill):
    fig, axes = plt.subplot_mosaic([['linear', 'linear-log'], ['log-linear', 'log-log']], layout='constrained')
    fig.suptitle(title)

    ax = axes['linear']
    ax.stairs(counts, bins, fill=fill)
    ax.set_xlabel('linear')
    ax.set_ylabel('linear')

    ax = axes['linear-log']
    ax.stairs(counts, bins, fill=fill)
    ax.set_yscale('log')
    ax.set_xlabel('linear')
    ax.set_ylabel('log')

    ax = axes['log-linear']
    ax.stairs(counts, bins, fill=True)
    ax.set_xscale('log')
    ax.set_xlabel('log')
    ax.set_ylabel('linear')

    ax = axes['log-log']
    ax.stairs(counts, bins, fill=True)
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel('log')
    ax.set_ylabel('log')


with open("wars.txt") as f:
    for line in f:
        line = line.replace('\n', '')
        tmp = line.split('\t')
        name.append(tmp[0])
        try:
            deaths.append(int(tmp[1]))
        except:
            print(tmp[1], "is a label")

bin_num = int((np.max(deaths) / dx))
deaths = arr.array('i', deaths)

counts, bins = np.histogram(deaths, bins=bin_num)
log_counts, log_bins = np.histogram(deaths, bins=np.logspace(3, 7, base=10, num=30))
# print(np.logspace(3, 7, base=10, num=30))
# print(counts)
tmp = np.logspace(3, 7, base=10, num=30)
bindwidths = np.zeros(log_counts.shape)
for i in range(len(log_bins) - 1):
    bindwidths[i] = tmp[i + 1] - tmp[i]
    # print(bindwidths[i])
# print(bindwidths)

plot_4_scales_hist(counts, bins, "Histogram - linear bins", False)
plot_4_scales_hist(counts / np.sum(counts), bins, "Probability - linear bins", False)
plot_4_scales_hist(log_counts, log_bins, "Histogram - logarithmic bins", False)
plot_4_scales_hist(log_counts / sum(log_counts) / bindwidths, log_bins, "Probability - logarithmic bins", False)
# print(sum(log_counts/bindwidths/sum(log_counts)))

cumulative = counts.copy() / np.sum(counts)
log_cumulative = log_counts.copy() / sum(log_counts) / bindwidths

for i in range(1, len(cumulative)):
    cumulative[i] = cumulative[i] + cumulative[i - 1]

for i in range(1, len(log_cumulative)):
    log_cumulative[i] = log_cumulative[i] + log_cumulative[i - 1]

plot_4_scales_hist(cumulative, bins, "Cumulative probability - linear bins", False)
plot_4_scales_hist(log_cumulative, log_bins, "Cumulative probability - logarithmic bins", False)

plt.show()
