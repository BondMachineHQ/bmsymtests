import pandas as pd
import matplotlib.pyplot as plt
import libs_data_processing as ldp

def plot_stats(gs,fragment):
    stats = (
        gs.loc[gs.index.str.startswith(fragment)]
        .assign(
            precision=lambda d: pd.to_numeric(
                d.index.to_series().str.extract(r'-(\d+)$')[0]
            ),
            bsimerror=lambda d: pd.to_numeric(d.bsimerror),
            bmerror=lambda d: pd.to_numeric(d.bmerror),
            bsimlatency=lambda d: pd.to_numeric(d.bsimlatency),
            bmlatency=lambda d: pd.to_numeric(d.bmlatency),
        )
        .dropna(subset=['precision'])
        .sort_values('precision')
    )

    if stats.empty:
        print(f"Nessun dato per {fragment}")
        return

    x = stats.precision.astype(int)
    fig, ax1 = plt.subplots(figsize=(10, 4))

    ax1.plot(x, stats.bsimerror, label='bsim error', color='#3a5a98', marker='o', linestyle=(0, (5,5)))
    ax1.plot(x, stats.bmerror, label='bm error', color='#e76f51', marker='o', linestyle=(0, (0,5,5,0)), markersize=4)
    ax1.set_yscale('log')
    ax1.set_xlabel('precision')
    ax1.set_ylabel('error')
    ax1.grid(True, which='both', ls='--', lw=0.5)
    plt.xticks(range(1, max(x)+1, max(1, max(x)//20)))

    ax2 = ax1.twinx()
    ax2.plot(x, stats.bsimlatency, label='bsim latency', color='#7b2cbf', marker='s')
    ax2.plot(x, stats.bmlatency, label='bm latency', color='#b11226', marker='s')
    ax2.set_ylabel('latency (clk cycles)')

    lines = ax1.get_lines() + ax2.get_lines()
    ax1.legend(lines, [l.get_label() for l in lines], fontsize='small', ncol=4, bbox_to_anchor=(0.5, -0.15))

    plt.title(fragment)
    plt.tight_layout()
    plt.show()

def plotHistogram(df):
	# Plot the histogram
	df['bsimoccurrences'].plot(kind='bar', figsize=(10, 6), color='skyblue')

def latencyHistogram(dataFile, latencyCol, title):
	df = pd.read_csv(dataFile)
	# Remove from df all but the last column
	df = df.iloc[:, -1:]
	df.columns = [latencyCol]
	import matplotlib.pyplot as plt

	plt.figure(figsize=(10, 6))
	plt.hist(df[latencyCol], bins=30, color='skyblue', edgecolor='black')
	plt.title(title)
	plt.xlabel('Latency')
	plt.ylabel('Frequency')
	plt.grid(True)
	plt.show()
	return plt.gcf()

def comparisonResultsPlot():
    # Extract latency columns for distribution comparison
	bsimDataDF=pd.read_csv('simbatch_outputs.csv')
	bmsimDataDF=pd.read_csv('bmsim_outputs.csv')
	# Extract just the latency column (last column)
	bsimData = bsimDataDF.iloc[:, -1]
	bmsimData = bmsimDataDF.iloc[:, -1]
	comparison_results = ldp.compareLatencyDistributions(bsimData, bmsimData)
	return comparison_results