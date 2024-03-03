#
# Building a Trading Robot in Python: https://www.youtube.com/playlist?list=PLcFcktZ0wnNmdgAdv4-Yl_nzS5LiKnhnn
# GitHub: https://github.com/areed1192/python-trading-robot
#

import numpy as np
import pandas as pd

# add here

long_series = pd.Series(np.random.randn(100))

print(long_series.head())
print(long_series.index)


# Define the MultiIndex levels
index_levels = [["Level1_A", "Level1_B"], ["Level2_A", "Level2_B", "Level2_C"]]
index_names = ["First Level", "Second Level"]
multi_index = pd.MultiIndex.from_product(index_levels, names=index_names)

# Initialize the DataFrame with random values
# Let's say we want a DataFrame with 3 columns
df = pd.DataFrame(
    np.random.rand(len(multi_index), 3),
    index=multi_index,
    columns=["Column1", "Column2", "Column3"],
)

# Now, let's group by one of the index dimensions, say the first level
grouped = df.groupby(
    level="First Level"
).mean()  # Using mean as an example aggregation function

print(df)
print(grouped)

amd = pd.read_csv(f"data/AMD.csv")
print(amd)

print(grouped.rolling(2))

print(locals())
