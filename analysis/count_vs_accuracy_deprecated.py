import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

if __name__ == '__main__':
	# data = {'model': [], 'himself_acc': [], 'herself_acc': [], 'themselves_acc': [],
	#         'himself_freq': [], 'herself_freq': [], 'themselves_freq': [],
	#         'himself_count': [], 'herself_count': [], 'themselves_count': []}


	# df = pd.read_csv('accuracy/all_exp_accuracy_tiny_rnng.csv')
	# df = df[df.model == 'rnng']
	# rnng_himself_acc = df[df.full_exp.str.contains('himself')].total_acc.mean()
	# rnng_herself_acc = df[df.full_exp.str.contains('herself')].total_acc.mean()
	# rnng_themselves_acc = df[df.full_exp.str.contains('pl')].total_acc.mean()

	# df = df[df.model == 'tiny']
	# tiny_himself_acc = df[df.full_exp.str.contains('himself')].total_acc.mean()
	# tiny_herself_acc = df[df.full_exp.str.contains('herself')].total_acc.mean()
	# tiny_themselves_acc = df[df.full_exp.str.contains('pl')].total_acc.mean()

	df = pd.read_csv('accuracy/all_exp_accuracy_grnn.csv')
	grnn_accuracies = []
	
	grnn_accuracies.append(df[df.full_exp.str.contains('herself')].total_acc.mean())
	grnn_accuracies.append(df[df.full_exp.str.contains('pl')].total_acc.mean())
	grnn_accuracies.append(df[df.full_exp.str.contains('himself')].total_acc.mean())
	# data['model'].append('grnn')
	# data['himself_acc'].append(df[df.full_exp.str.contains('himself')].total_acc.mean())
	# data['herself_acc'].append(df[df.full_exp.str.contains('herself')].total_acc.mean())
	# data['themselves_acc'].append(df[df.full_exp.str.contains('pl')].total_acc.mean())

	# WIKIPEDIA
	wiki_himself_freq = 0.6 #float(61 / 101)
	wiki_herself_freq = 0.8
	wiki_themselves_freq = 0.73

	wiki_himself_count = 17226
	wiki_herself_count = 3688
	wiki_themselves_count = 9670

	wiki_freqs = [wiki_himself_freq, wiki_themselves_freq, wiki_herself_freq]
	wiki_counts = [wiki_herself_count, wiki_themselves_count, wiki_himself_count]

	pronouns = ['herself', 'themselves', 'himself']

	# data['himself_freq'].append(wiki_himself_freq)
	# data['herself_freq'].append(wiki_herself_freq)
	# data['themselves_freq'].append(wiki_themselves_freq)
	# data['himself_count'].append(wiki_himself_count)
	# data['herself_count'].append(wiki_herself_count)
	# data['themselves_count'].append(wiki_themselves_count)

	sns.set_style('ticks')
	plt.rcParams.update({'font.size': 22})

	_, axes = plt.subplots(nrows=1, ncols=2, figsize=(13, 7), sharey=True)
	plt.subplots_adjust(wspace=0.1)
	l_ax, r_ax = axes

	l_ax = sns.pointplot(x=wiki_counts, y=grnn_accuracies, ax=l_ax)

	for i, pn in enumerate(pronouns):
		l_ax.annotate(pn, (i, grnn_accuracies[i]), size='small', xytext=(10, 0), textcoords="offset points")

	grnn_accuracies.reverse()
	pronouns.reverse()
	r_ax = sns.pointplot(x=wiki_freqs, y=grnn_accuracies, ax=r_ax)
	for i, pn in enumerate(pronouns):
		r_ax.annotate(pn, (i, grnn_accuracies[i]), size='small', xytext=(10, 0), textcoords="offset points")

	l_ax.set_ylabel('accuracy (avg over experiments)')
	l_ax.set_xlabel('raw count')
	l_ax.set_title('accuracy vs. raw count')
	r_ax.set_xlabel('relative frequency')
	r_ax.set_title('accuracy vs. relative freq.')
	
	plt.savefig('acc_grnn.pdf', bbox_inches='tight')

	# PTB
	# ptb_himself_freq = float(60 / 95)
	# ptb_herself_freq = float(9 / 12)
	# ptb_themselves_freq = float(89 / 114)
	# ptb_himself_count = 95
	# ptb_herself_count = 12
	# ptb_themselves_count = 114

	# _, axes = plt.subplots(nrows=2, ncols=2)
	# ax = axes[0,0]
	# ax.scatter([wiki_himself_count, wiki_herself_count, wiki_themselves_count], [grnn_himself_acc, grnn_herself_acc, grnn_themselves_acc])
	# ax.set_xlabel('count')
	# ax.set_ylabel('mean accuracy')
	# ax.set_title('wiki/grnn count')

	# ax = axes[0,1]
	# ax.scatter([ptb_himself_count, ptb_herself_count, ptb_themselves_count], [rnng_himself_acc, rnng_herself_acc, rnng_themselves_acc])
	# ax.set_xlabel('count')
	# ax.set_ylabel('mean accuracy')
	# ax.set_title('ptb/rnng count')

	# ax = axes[1,0]
	# ax.scatter([wiki_himself_freq, wiki_herself_freq, wiki_themselves_freq], [grnn_himself_acc, grnn_herself_acc, grnn_themselves_acc])
	# ax.set_xlabel('freq')
	# ax.set_ylabel('mean accuracy')
	# ax.set_title('wiki/grnn freq')

	# ax = axes[1,1]
	# ax.scatter([ptb_himself_freq, ptb_herself_freq, ptb_themselves_freq], [rnng_himself_acc, rnng_herself_acc, rnng_themselves_acc])
	# ax.set_xlabel('freq')
	# ax.set_ylabel('mean accuracy')
	# ax.set_title('ptb/rnng freq')

	# plt.show()


