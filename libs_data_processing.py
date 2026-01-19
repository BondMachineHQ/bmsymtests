import numpy as np
import pandas as pd
import sklearn.metrics
from scipy import stats
import matplotlib.pyplot as plt
import os
import json

def loadGlobalStats():
	# Load the global statistics from the CSV file if it exists
	if os.path.exists('global_statistics'):
		global_stats = pd.read_csv('global_statistics', index_col=0)
		global_stats.sort_index(inplace=True)
	else:
		# Create an empty DataFrame with the same columns as the global statistics
		global_stats = pd.DataFrame(columns=['bsimoccurrences', 'bsimerror', 'bmoccurrences', 'bmerror','bmlatency', 'bsimlatency'])
	return global_stats

# Analyze Simbatch results
def analyzeSimbatch(benchcore):
	# Load the target outputs from the output.csv file
	targetData = np.loadtxt('outputs.csv', delimiter=',')
	simbatchData = np.loadtxt('simbatch_outputs.csv', delimiter=',')
	latency = False

	if benchcore:
		benchcoreData = simbatchData[:, -1]
		# Move the last column,if there is a benchcore
		simbatchData = np.delete(simbatchData, -1, axis=1)

	simbatchMSE=sklearn.metrics.mean_squared_error(targetData, simbatchData)
	if benchcore:
		latency = benchcoreData.mean()
		data = {
			"Dataset": ["Sympy target", "Simbatch","Latency"],
			"MSE" : [0.0, simbatchMSE, latency]
		}
	else:
		data = {
			"Dataset": ["Sympy target", "Simbatch"],
			"MSE" : [0.0, simbatchMSE]
		}
	df = pd.DataFrame(data)
	return df.style.hide(axis="index"), simbatchMSE, latency

# Analyze the hardware simulation results
def analyzeBMsim(benchcore):
	# Load the target outputs from the output.csv file
	targetData = np.loadtxt('outputs.csv', delimiter=',')
	bmsimData = np.loadtxt('bmsim_outputs.csv', delimiter=',')
	latency = False

	if benchcore:
		benchcoreData = bmsimData[:, -1]
		# Move the last column,if there is a benchcore
		bmsimData = np.delete(bmsimData, -1, axis=1)

	bmsimMSE=sklearn.metrics.mean_squared_error(targetData, bmsimData)

	if benchcore:
		latency = benchcoreData.mean()
		data = {
			"Dataset": ["Sympy target", "BMsim","Latency"],
			"MSE" : [0.0, bmsimMSE, latency]
		}
	else:
		data = {
			"Dataset": ["Sympy target", "BMsim"],
			"MSE" : [0.0, bmsimMSE]
		}
	df = pd.DataFrame(data)
	return df.style.hide(axis="index"), bmsimMSE, latency

# Load BMsim run statistics
def loadBsimRun(mse,latency):
	with open('statistics.json', 'r') as f:
		data = json.load(f)
	
	df = pd.DataFrame.from_dict(data, orient='index', columns=['bsimoccurrences'])
	totOccurrences = df['bsimoccurrences'].sum()
	newCol=mse
	if totOccurrences > 0:
		newCol = newCol/totOccurrences
		df['bsimerror'] = newCol
	else:
		df['bsimerror'] = 0.0
	if latency:
		df['bsimlatency'] = latency
	
	return df

# Load BMsim run statistics
def loadBMsimRun(mse,latency):
	with open('statistics.json', 'r') as f:
		data = json.load(f)
	
	df = pd.DataFrame.from_dict(data, orient='index', columns=['bmoccurrences'])
	totOccurrences = df['bmoccurrences'].sum()
	newCol=mse
	if totOccurrences > 0:
		newCol = newCol/totOccurrences
		df['bmerror'] = newCol
	else:
		df['bmerror'] = 0.0
	if latency:
		df['bmlatency'] = latency
	return df

def compareLatencyDistributions(bsimData, bmsimData):
	"""
	Compare two latency distributions using statistical tests and visualizations.
	
	Args:
		bsimData: pandas Series of Simbatch latencies
		bmsimData: pandas Series of BMsim latencies
	
	Returns:
		Dictionary with comparison results
	"""
	
	results = {}
	
	# 1. Descriptive Statistics
	results['bsim_stats'] = {
		'mean': bsimData.mean(),
		'median': bsimData.median(),
		'std': bsimData.std(),
		'min': bsimData.min(),
		'max': bsimData.max(),
		'q25': bsimData.quantile(0.25),
		'q75': bsimData.quantile(0.75)
	}
	
	results['bmsim_stats'] = {
		'mean': bmsimData.mean(),
		'median': bmsimData.median(),
		'std': bmsimData.std(),
		'min': bmsimData.min(),
		'max': bmsimData.max(),
		'q25': bmsimData.quantile(0.25),
		'q75': bmsimData.quantile(0.75)
	}
	
	# 2. Statistical Tests
	# Kolmogorov-Smirnov Test (are distributions different?)
	ks_stat, ks_pvalue = stats.ks_2samp(bsimData, bmsimData)
	results['ks_test'] = {
		'statistic': ks_stat,
		'p_value': ks_pvalue,
		'significant': ks_pvalue < 0.05
	}
	
	# Mann-Whitney U Test (non-parametric comparison of medians)
	mw_stat, mw_pvalue = stats.mannwhitneyu(bsimData, bmsimData, alternative='two-sided')
	results['mann_whitney'] = {
		'statistic': mw_stat,
		'p_value': mw_pvalue,
		'significant': mw_pvalue < 0.05
	}
	
	# Wasserstein Distance (Earth Mover's Distance)
	wasserstein = stats.wasserstein_distance(bsimData, bmsimData)
	results['wasserstein_distance'] = wasserstein
	
	# 3. Visualizations
	fig, axes = plt.subplots(2, 2, figsize=(14, 10))
	
	# Overlaid histograms
	axes[0, 0].hist(bsimData, bins=30, alpha=0.5, label='Simbatch', color='blue', edgecolor='black')
	axes[0, 0].hist(bmsimData, bins=30, alpha=0.5, label='BMsim', color='red', edgecolor='black')
	axes[0, 0].set_xlabel('Latency')
	axes[0, 0].set_ylabel('Frequency')
	axes[0, 0].set_title('Overlaid Histograms')
	axes[0, 0].legend()
	axes[0, 0].grid(True, alpha=0.3)
	
	# Box plots
	axes[0, 1].boxplot([bsimData, bmsimData], labels=['Simbatch', 'BMsim'])
	axes[0, 1].set_ylabel('Latency')
	axes[0, 1].set_title('Box Plot Comparison')
	axes[0, 1].grid(True, alpha=0.3)
	
	# Cumulative Distribution Functions
	axes[1, 0].hist(bsimData, bins=50, cumulative=True, alpha=0.5, label='Simbatch', 
	                color='blue', edgecolor='black', density=True)
	axes[1, 0].hist(bmsimData, bins=50, cumulative=True, alpha=0.5, label='BMsim', 
	                color='red', edgecolor='black', density=True)
	axes[1, 0].set_xlabel('Latency')
	axes[1, 0].set_ylabel('Cumulative Probability')
	axes[1, 0].set_title('Cumulative Distribution Functions')
	axes[1, 0].legend()
	axes[1, 0].grid(True, alpha=0.3)
	
	# Q-Q Plot
	quantiles = np.linspace(0, 1, min(len(bsimData), len(bmsimData)))
	bsim_quantiles = bsimData.quantile(quantiles)
	bmsim_quantiles = bmsimData.quantile(quantiles)
	axes[1, 1].scatter(bsim_quantiles, bmsim_quantiles, alpha=0.5)
	min_val = min(bsim_quantiles.min(), bmsim_quantiles.min())
	max_val = max(bsim_quantiles.max(), bmsim_quantiles.max())
	axes[1, 1].plot([min_val, max_val], [min_val, max_val], 'r--', label='Perfect match')
	axes[1, 1].set_xlabel('Simbatch Quantiles')
	axes[1, 1].set_ylabel('BMsim Quantiles')
	axes[1, 1].set_title('Q-Q Plot')
	axes[1, 1].legend()
	axes[1, 1].grid(True, alpha=0.3)
	
	plt.tight_layout()
	plt.show()
	
	# Print summary
	print("="*60)
	print("LATENCY DISTRIBUTION COMPARISON")
	print("="*60)
	print(f"\nSimbatch Statistics:")
	print(f"  Mean: {results['bsim_stats']['mean']:.4f}")
	print(f"  Median: {results['bsim_stats']['median']:.4f}")
	print(f"  Std Dev: {results['bsim_stats']['std']:.4f}")
	print(f"  Range: [{results['bsim_stats']['min']:.4f}, {results['bsim_stats']['max']:.4f}]")
	
	print(f"\nBMsim Statistics:")
	print(f"  Mean: {results['bmsim_stats']['mean']:.4f}")
	print(f"  Median: {results['bmsim_stats']['median']:.4f}")
	print(f"  Std Dev: {results['bmsim_stats']['std']:.4f}")
	print(f"  Range: [{results['bmsim_stats']['min']:.4f}, {results['bmsim_stats']['max']:.4f}]")
	
	print(f"\nStatistical Tests:")
	print(f"  Kolmogorov-Smirnov Test:")
	print(f"    Statistic: {results['ks_test']['statistic']:.4f}")
	print(f"    P-value: {results['ks_test']['p_value']:.4e}")
	print(f"    Distributions are {'DIFFERENT' if results['ks_test']['significant'] else 'SIMILAR'} (α=0.05)")
	
	print(f"\n  Mann-Whitney U Test:")
	print(f"    Statistic: {results['mann_whitney']['statistic']:.4f}")
	print(f"    P-value: {results['mann_whitney']['p_value']:.4e}")
	print(f"    Medians are {'DIFFERENT' if results['mann_whitney']['significant'] else 'SIMILAR'} (α=0.05)")
	
	print(f"\n  Wasserstein Distance: {results['wasserstein_distance']:.4f}")
	print(f"    (Lower is better, 0 = identical distributions)")
	print("="*60)
	
	return results

def PatchBsimGlobalStats(global_stats, df):
	# If the global statistics DataFrame is empty, initialize it with the same rows as the current DataFrame
	for index, row in df.iterrows():
		if index not in global_stats.index:
			global_stats.loc[index] = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

	# Sum the occurrences to the global statistics
	for index, row in df.iterrows():
		if row['bsimoccurrences'] > 0:
			firstRun=False
			if global_stats.at[index, 'bsimoccurrences'] == 0:
				firstRun=True
			sumErrors=global_stats.at[index, 'bsimoccurrences'] * global_stats.at[index, 'bsimerror'] + row['bsimerror']
			if 'bsimlatency' in row and (global_stats.at[index, 'bsimlatency']>0.0 or firstRun):
				sumLatencies=global_stats.at[index, 'bsimoccurrences'] * global_stats.at[index, 'bsimlatency'] + row['bsimlatency']
			global_stats.at[index, 'bsimoccurrences'] += row['bsimoccurrences']
			global_stats.at[index, 'bsimerror'] = sumErrors / global_stats.at[index, 'bsimoccurrences']
			if 'bsimlatency' in row and (global_stats.at[index, 'bsimlatency']>0.0 or firstRun):
				global_stats.at[index, 'bsimlatency'] = sumLatencies / global_stats.at[index, 'bsimoccurrences']

	# Save the updated global statistics
	global_stats.to_csv('global_statistics')
	return global_stats

def PatchBMsimGlobalStats(global_stats, df):
	# If the global statistics DataFrame is empty, initialize it with the same rows as the current DataFrame
	for index, row in df.iterrows():
		if index not in global_stats.index:
			global_stats.loc[index] = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

	# Sum the occurrences to the global statistics
	for index, row in df.iterrows():
		if row['bmoccurrences'] > 0:
			firstRun=False
			if global_stats.at[index, 'bmoccurrences'] == 0:
				firstRun=True
			sumErrors=global_stats.at[index, 'bmoccurrences'] * global_stats.at[index, 'bmerror'] + row['bmerror']
			if 'bmlatency' in row and (global_stats.at[index, 'bmlatency']>0.0 or firstRun):
				sumLatencies=global_stats.at[index, 'bmoccurrences'] * global_stats.at[index, 'bmlatency'] + row['bmlatency']
			global_stats.at[index, 'bmoccurrences'] += row['bmoccurrences']
			global_stats.at[index, 'bmerror'] = sumErrors / global_stats.at[index, 'bmoccurrences']
			if 'bmlatency' in row and (global_stats.at[index, 'bmlatency']>0.0 or firstRun):
				global_stats.at[index, 'bmlatency'] = sumLatencies / global_stats.at[index, 'bmoccurrences']

	# Save the updated global statistics
	global_stats.to_csv('global_statistics')
	return global_stats