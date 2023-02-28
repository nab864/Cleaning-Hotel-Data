import django
import numpy as np
import pandas as pd

df1 = pd.read_csv('H1.csv')
df2 = pd.read_csv('H2.csv')
df = pd.concat([df1,df2])


