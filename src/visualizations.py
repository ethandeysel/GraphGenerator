import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import io

def get_pillar_chart(row_data, averages):
    cols = list(averages.columns)[1:] # Remove risk rating
    row_val = row_data[cols]
    avgs = averages.iloc[0][cols]
    
    cmap = plt.get_cmap('tab20')
    bar_colours = [cmap(i) for i in range(7)]
    bar_colours[-1] = "#F29CFF"

    fig, ax = plt.subplots(figsize=(12, 7))
    
    for i, col in enumerate(cols):
        ax.hlines(avgs[col], i - 0.4, i + 0.4, colors='red', linewidth=2)
        ax.text(i, row_val[col] / 2, f"{row_val[col]:.1f}", ha='center', fontsize=10)

    ax.set_title(f"{row_data['SUPPLIER']} Pillar Scores vs Group Average")
    ax.set_ylim(0, 105)
    ax.set_xticks(range(7))
    ax.set_xticklabels(['A', 'B', 'C', 'D', 'E', 'F', 'G'])
    
    return fig

def get_risk_bar(row_data, avg_risk):
    val = row_data['Risk Rating ']
    
    # colour logic
    def get_color(x):
        if x < 1: return '#ED009F'
        if x < 2: return '#FF908A'
        if x < 3: return '#FFB742'
        if x < 4: return '#8AFF93'
        return '#26C700'

    fig, ax = plt.subplots(figsize=(10, 2))
    ax.barh(['Risk Rating'], [val], color=get_color(val), height=0.4)
    ax.axvline(avg_risk, color='red', linewidth=2, label='Avg')
    ax.set_xlim(0, 5)
    ax.set_title(f"Risk Rating: {row_data['SUPPLIER']}")
    
    return fig