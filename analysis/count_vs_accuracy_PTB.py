import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import seaborn as sns

ptb_freqs = {
	'himself' : float(60 / 95),
	'herself' : float(9 / 12),
	'themselves' : float(89 / 114)
}
ptb_counts = {
	'himself' : 95,
	'herself' : 12,
	'themselves' : 114,
}
wiki_freqs = {
	'himself': float(61 / 101),
	'herself': 0.8,
	'themselves': 0.73,
}
wiki_counts = {
	'himself' : 17226,
	'herself' : 3688,
	'themselves' : 9670,
}


def save_df(path, ptb_model='tiny'):
	pronouns = ['herself', 'themselves', 'himself']

	data = {'model': [], 'pronoun': [], 'acc': [], 'freq': [], 'count': []}

	# PTB!!!!!!!!!!!!!!!!!
	df = pd.read_csv('accuracy/all_exp_accuracy_tiny_rnng.csv')
	df = df[df.model == ptb_model]
	for pn in pronouns:
		data['model'].append(ptb_model)
		data['pronoun'].append(pn)
		exp_pn = pn if pn != 'themselves' else 'pl'
		data['acc'].append(df[df.full_exp.str.contains(exp_pn)].total_acc.mean())
		data['freq'].append(ptb_freqs[pn])
		data['count'].append(ptb_counts[pn])

	# WIKIPEDIA!!!!!!!!!!!
	df = pd.read_csv('accuracy/all_exp_accuracy_grnn.csv')
	df = df[df.model == 'grnn']
	for pn in pronouns:
		data['model'].append('grnn')
		data['pronoun'].append(pn)
		exp_pn = pn if pn != 'themselves' else 'pl'
		data['acc'].append(df[df.full_exp.str.contains(exp_pn)].total_acc.mean())
		data['freq'].append(wiki_freqs[pn])
		data['count'].append(wiki_counts[pn])

	data_df = pd.DataFrame(data)
	data_df.to_csv(path, index=False)

def annotate(axes):
	params = dict(
		textcoords="offset points"
	)

	grnn_count = axes[0,0]
	grnn_freq = axes[0,1]
	tiny_count = axes[1,0]
	tiny_freq = axes[1,1]

	grnn_count.annotate('herself', (0, 0.9180952380952381), xytext=(20,-10), **params)
	grnn_count.annotate('themselves', (1, 0.8573809523809524), xytext=(10,0), **params)
	grnn_count.annotate('himself', (2, 0.8061904761904761), xytext=(-80,0), **params)

	grnn_freq.annotate('herself', (2, 0.9180952380952381), xytext=(-60,-10), **params)
	grnn_freq.annotate('themselves', (1, 0.8573809523809524), xytext=(20,0), **params)
	grnn_freq.annotate('himself', (0, 0.8061904761904761), xytext=(20,0), **params)

	tiny_count.annotate('herself', (0, 0.27555555555555555), xytext=(20,0), **params)
	tiny_count.annotate('himself', (1, 0.43111111111111106), xytext=(20,0), **params)
	tiny_count.annotate('themselves', (2, 0.6533333333333333), xytext=(-100,-10), **params)

	tiny_freq.annotate('himself', (0, 0.43111111111111106), xytext=(-10,10), **params)
	tiny_freq.annotate('herself', (1, 0.27555555555555555), xytext=(20,0), **params)
	tiny_freq.annotate('themselves', (2, 0.6533333333333333), xytext=(-100,-10), **params)

	return axes

def plot(df):
	sns.set_style('ticks')
	plt.rcParams.update({'font.size': 16})
	models = ['grnn', 'tiny']
	model_titles = ['Wiki / GRNN', 'PTB / TinyLSTM']
	colors = ['green', 'orange']

	_, axes = plt.subplots(nrows=2, ncols=2, sharey='row', figsize=(9,8))
	plt.subplots_adjust(hspace=0.2, wspace=0.1)
	for i in range(2):
		for j in range(2):
			ax = axes[i,j]
			model = models[i]
			model_title = model_titles[i]
			model_df = df[df.model == model]
			x = 'count' if j == 0 else 'freq'
			sns.pointplot(data=model_df, x=x, y='acc', ax=ax, color=colors[i], scale=1.5)
			if i == 0:
				ax.set_xlabel('')
			else:
				if j == 0:
					ax.set_xlabel('# occurrences in corpus')
				else:
					ax.set_xlabel('relative freq. of anaphor usage')
			if j == 0:
				if i == 0:
					ax.set_title('accuracy vs. raw count')
				ax.set_ylabel('accuracy')
				ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
			else:
				if i == 0:
					ax.set_title('accuracy vs. anaphor freq.')
				ax.yaxis.set_label_position("right")
				ax.set_ylabel(model_title, labelpad=25, fontweight='bold', size='large', rotation=270)
				xticklabels = ax.get_xticklabels()
				rounded_labels = [str(round(float(l.get_text()), 2)) for l in xticklabels]
				ax.set_xticklabels(rounded_labels)

	axes = annotate(axes)

	plt.savefig('acc_freq.pdf', bbox_inches='tight')

if __name__ == '__main__':
	save_df('acc_freq_data.csv')
	df = pd.read_csv('acc_freq_data.csv')
	plot(df)


