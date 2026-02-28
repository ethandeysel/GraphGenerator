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
    bars = ax.bar(cols, row_val, color=bar_colours)
    
    for i, col in enumerate(cols):
        ax.hlines(avgs[col], i - 0.4, i + 0.4, colors='red', linewidth=2)
        ax.text(i, row_val[col] / 2, f"{row_val[col]:.1f}", ha='center', fontsize=10)
    bar_legend = [mpatches.Patch(color=bar_colours[i], label=cols[i]) for i in range(7)]
    avg_patch = mpatches.Patch(color='red', label='Group Average')
    ax.set_title(f"{row_data['SUPPLIER']} Pillar Scores vs Group Average")
    ax.set_ylim(0, 105)
    plt.legend(handles=[avg_patch] + bar_legend, loc='center left', fontsize=15, bbox_to_anchor=(1.02, 0.5))
    ax.set_xticks(range(7))
    ax.set_xticklabels(['A', 'B', 'C', 'D', 'E', 'F', 'G'])
    fig.tight_layout()
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
    avg_patch = mpatches.Patch(color='red', label='Group Average')
    color_legend = [
        mpatches.Patch(color='#26C700', label='Low'),
        mpatches.Patch(color='#8AFF93', label='Low-Medium'),
        mpatches.Patch(color='#FFB742', label='Medium'),
        mpatches.Patch(color='#FF908A', label='High'),
        mpatches.Patch(color='#ED009F', label='Critical')
    ]
    fig, ax = plt.subplots(figsize=(10, 2))
    plt.text(1*val/2,0, f"{val:.2f}", ha='center', va='center', fontsize=9)
    plt.legend(handles=[avg_patch] + color_legend,
               loc='center left', bbox_to_anchor=(1.02, 0.5), fontsize=9)
    ax.barh(['Risk Rating'], [val], color=get_color(val), height=0.4)
    ax.axvline(avg_risk, color='red', linewidth=2, label='Avg')
    ax.set_xlim(0, 5)
    ax.set_title(f"Risk Rating: {row_data['SUPPLIER']}")
    fig.tight_layout()
    return fig