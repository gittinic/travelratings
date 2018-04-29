import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

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


def country_pie_chart(country: str):
    if check_country(country):
        # Get data
        dat = feat[feat['Country'] == country]
        scores = dat[score_list].values[0]
        total = dat['Total'].values
        rank = dat['Rank'].values
        labels = score_list

        # Plot
        def absolute_value(val):
            a = np.round(val / 100. * scores.sum(), 0)
            return a

        plt.figure(figsize=(6, 6))
        plt.pie(scores, labels=labels, autopct=absolute_value)
        plt.axis('equal')
        plt.title('Country: %(country)s overall scores %(total)d and ranks %(rank)d \n\n'
                  % {'country': country, 'total': total, 'rank': rank})
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