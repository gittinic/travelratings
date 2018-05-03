import pandas as pd
from scipy.stats import norm
import numpy as np

# Read data
raw = pd.read_excel('data.xlsx', sheet_name='merged', header=0)


'''
Generate features:
The idea is to have each feature on a scale from 0 to 10.
If the values were evenly distributed then we could simple use scale_10 and divide each value by its max or min 
depending on what is better. However, when countries have very similar values except there is only one outlier,
then this scaling can distort the information, i.e. extreme scores at the tails. 
That is why each variable is first standardize as if it were normally distributed. Since the normal distribution is 
symmetric, the goal (min, max) can achieved by mirroring the values if necessary (multiplication by -1). 
After that, the cumulative probability is computed for each normalized z which will be between [0,1]. Finally,
to achieve a 0 to 10 scale, this value is multiplied by 10.

The total score is computed as the sum of the individual scores.
'''


def feat_per_head(feat):
    feat_ph = feat / raw['population']
    return feat_ph


def scale(x: float, goal: str):
    # Normalize variable
    mean = x.mean()
    sd = x.std()
    z = (x - mean) / sd

    # If goal is to minimize --> mirror
    if goal == 'min':
        z = -1 * z
    elif goal == 'max':
        z = z
    else:
        return 'Invalid goal!'

    # Compute cdf from x
    y = np.array([norm(0,1).cdf(i) for i in z])

    # Make 0 to 10 scale
    y10 = y * 10

    # Round to 1 digit for better presentation
    y10 = np.round(y10, decimals=1)
    return y10


def total_score_df(df):
    df['Total'] = df.sum(axis=1)
    return df


def comp_rank(df):
    df['Rank'] = np.floor(df['Total'].rank(ascending=False))
    return df


# Compute tourism per head
tour = feat_per_head(raw['tourism'])
attacks = feat_per_head(raw['attacks'])

# Scale data
tour = scale(tour, 'min')
attacks = scale(attacks, 'min')
living_costs = scale(raw['cost_of_living'], 'min')

# Create feature data frame
features = pd.DataFrame({'Country': raw['country'], 'Tourism': tour, 'Safety': attacks, 'Affordability': living_costs})

# Compute total score
features = total_score_df(features)
features = comp_rank(features)

# Set order in data frame
features = features[['Country', 'Affordability', 'Safety', 'Tourism', 'Total', 'Rank']]

# Set order in data frame
features = features[['Country', 'Affordability', 'Safety', 'Tourism', 'Total', 'Rank']]

writer = pd.ExcelWriter('features.xlsx')
features.to_excel(writer,'Features', index=False)
writer.save()
