import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

feat = pd.read_excel('features.xlsx', sheet_name='Features', header=0)

def bar_plot_score(score, top):
    # Sort and subset data
    feat_sort = feat.sort_values(by=[score], ascending=False)
    feat_subset = feat_sort[:top]
    print(len(feat_subset[score]))
    ind = np.arange(top)

    # Create bar
    plt.figure(figsize=(15, 10))
    plt.bar(ind, feat_subset[score])

    # Plot labeling
    plt.title('Top ' + str(top) + ' Countries regarding ' + score)
    plt.ylabel('Score')
    plt.xticks(ind, feat_subset['Country'], rotation=45)
    plt.ylim([0, 10])
    for i, v in enumerate(feat_subset[score]):
        plt.text(i, v + .25, str(v), color='black')
    plt.show()


def stacked_bar_plot_total_score(top):
    # Sort and subset data
    feat_sort = feat.sort_values(by=['Total'], ascending=False)
    feat_subset = feat_sort[:top]
    ind = np.arange(top)

    y1 = feat_subset['Affordability']
    y2 = feat_subset['Safety']
    y3 = feat_subset['Tourism']

    # Create bars
    plt.figure(figsize=(15, 10))
    p1 = plt.bar(ind, y1, color='#F08080')
    p2 = plt.bar(ind, y2, color='#F0E68C', bottom=y1)
    p3 = plt.bar(ind, y3, color='#8FBC8B', bottom=y1+y2)

    # Plot labeling
    for i, v in enumerate(feat_subset['Total']):
        plt.text(i, v + .5, str(v), color='black')
    plt.ylabel('Scores')
    plt.title('Top ' + str(top) + ' Countries regarding ' + 'Aggregated Score')
    plt.xticks(ind, feat_subset['Country'], rotation=45)
    plt.ylim([0, 30])
    plt.legend((p1[0], p2[0], p3[0]), ('Affordability', 'Safety', 'Tourism'))
    plt.show()

def group_bar_plot():
    # Get data from top-5 countries
    top = feat.sort_values(['Rank'], ascending=[True])
    indices = top[:5][['Country', 'Affordability', 'Safety', 'Tourism', ]]
    # Plot
    plot = indices.plot.bar()
    # Set format
    plot.set_ylim([0, 10])
    plot.set_ylabel('Scores')
    plot.set_xticklabels(indices['Country'], rotation=0)
    plot.set_title('Indices from top 5 countries')
    plt.grid(linestyle='dotted')
    plt.show()

# bar_plot_score('Affordability',100)
# group_bar_plot()