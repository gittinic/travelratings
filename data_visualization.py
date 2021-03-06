import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from requests import get

# Change matplotlib plot style
plt.style.use('ggplot')


# Global data
feat = pd.read_excel('features.xlsx', sheet_name='Features', header=0)
score_list = ['Affordability', 'Safety', 'Tourism']
country_list = list(feat['Country'])


# Helper functions
def check_score(score):
    if score in score_list:
        return True
    else:
        return False


def print_score_error(score):
    print('%(score)s does not exist. Please specify a valid score name.' % {'score': score})


def check_country(country):
    if country in country_list:
        return True
    else:
        return False

def print_country_error(country):
    print('%(country)s does not exist or has no data. Please check spelling or choose a different country.' % {'country': country})



# Visualizations


def bar_plot_score(score: str, top: int):
    if check_score(score):
        # Sort and subset data
        feat_sort = feat.sort_values(by=[score], ascending=False)
        feat_subset = feat_sort[:top]
        ind = np.arange(top)

        # Create bar
        plt.figure(figsize=(10, 7))
        plt.bar(ind, feat_subset[score])

        # Plot labeling
        plt.title('Top ' + str(top) + ' Countries regarding ' + score)
        plt.ylabel('Score')
        plt.xticks(ind, feat_subset['Country'], rotation=45)
        plt.ylim([0, 10])
        for i, v in enumerate(feat_subset[score]):
            plt.text(i, v + .25, str(v), color='black')
        plt.show()
    else:
        print_score_error(score)


def stacked_bar_plot_total_score(top: int):
    # Sort and subset data
    feat_sort = feat.sort_values(by=['Total'], ascending=False)
    feat_subset = feat_sort[:top]
    ind = np.arange(top)

    y1 = feat_subset['Affordability']
    y2 = feat_subset['Safety']
    y3 = feat_subset['Tourism']

    # Create bars
    plt.figure(figsize=(10, 7))
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

def country_pie_chart(country: str):
    if check_country(country):
        # Get data
        dat = feat[feat['Country'] == country]
        scores = dat[score_list].values[0].tolist()
        total = float(dat['Total'].values)
        rank = dat['Rank'].values
        labels = score_list

        # Get user data
        feedback_available = False
        try:
            affordability = get('http://localhost:5000/feedback/Affordability/%s' % country).json()
            safety = get('http://localhost:5000/feedback/Safety/%s' % country).json()
            tourism = get('http://localhost:5000/feedback/Tourism/%s' % country).json()
            scores_user = [np.mean(affordability), np.mean(safety), np.mean(tourism)]
            total_user = np.sum(scores_user)
            feedback_available = True
        except:
            feedback_available = False

        # Plot data sources
        if feedback_available:
            plt.figure(figsize=(12, 6))
            plt.subplot(1, 2, 1)
        else:
            plt.figure(figsize=(6, 6))
        plt.pie(scores, labels=labels, autopct=lambda p: round(p * total / 100, 1))
        plt.axis('equal')
        plt.title('%(country)s scores %(total)8.1f and ranks %(rank)d \n\n'
                  % {'country': country, 'total': total, 'rank': rank})

        # Plot for feedback
        if feedback_available:
            plt.subplot(1, 2, 2)
            plt.pie(scores_user, labels=labels, autopct=lambda p: round(p * total_user / 100, 1))
            plt.axis('equal')
            plt.title('Users give %(country)s a score of %(total)8.1f \n\n'
                      % {'country': country, 'total': total_user})

        plt.tight_layout()
        plt.show()
    else:
        print_country_error(country)


def country_score_tbl(score: str, top: int):
    if check_score(score) or score == 'Total':
        print(feat.sort_values(by=[score], ascending=False)[:top+1])
    else:
        print_score_error(score)


def country_score(country: str):
    if check_country(country):
        print(feat[feat['Country'] == country])
    else:
        print_country_error(country)

# def score_surface_plot():
#     fig = plt.figure()
#     ax = fig.gca(projection='3d')
#     X, Y = np.meshgrid(feat['Affordability'], feat['Tourism'])
#     R = np.sqrt(X ** 2 + Y ** 2)
#     Z = np.sin(R) / (X ** 2 + Y ** 2)
#     # Plot the surface.
#     surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,
#                            linewidth=0, antialiased=False)
#     # Customize the z axis.
#     ax.set_zlim(0, 10)
#     ax.zaxis.set_major_locator(LinearLocator(10))
#     ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
#     ax.set_zlabel('Distance', fontsize=5, rotation=0)
#
#     # Customize the labels
#     ax.set_xlabel('Affordability', fontsize=7)
#     ax.set_ylabel('Tourism', fontsize=7)
#     for tick in ax.xaxis.get_major_ticks():
#         tick.label.set_fontsize(5)
#     for tick in ax.yaxis.get_major_ticks():
#         tick.label.set_fontsize(5)
#     for tick in ax.zaxis.get_major_ticks():
#         tick.label.set_fontsize(5)
#     # Add a color bar which maps values to colors.
#     fig.colorbar(surf, shrink=0.5, aspect=5)
#     plt.title('Relation Analysis')
#     plt.show()

def score_plot_trisurf():
    fig = plt.figure()
    ax = fig.gca(projection='3d')

    ax.plot_trisurf(feat['Affordability'], feat['Tourism'], feat['Safety'], linewidth=0.2, antialiased=True)

    # Customize the z axis.
    ax.set_zlim(0, 10)
    ax.zaxis.set_major_locator(LinearLocator(10))
    ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
    ax.set_zlabel('Safety', fontsize=5, rotation=0)

    # Customize the labels
    ax.set_xlabel('Affordability', fontsize=7)
    ax.set_ylabel('Tourism', fontsize=7)
    for tick in ax.xaxis.get_major_ticks():
        tick.label.set_fontsize(5)
    for tick in ax.yaxis.get_major_ticks():
        tick.label.set_fontsize(5)
    for tick in ax.zaxis.get_major_ticks():
        tick.label.set_fontsize(5)

    plt.title('Relationship among indices')
    plt.show()

# score_plot_trisurf()
# score_surface_plot()
# bar_plot_score('Affordability',100)
# group_bar_plot()
# country_pie_chart('Japan')
# country_score_tbl('12.9', 50)