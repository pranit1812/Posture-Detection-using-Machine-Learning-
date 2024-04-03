# -*- coding: utf-8 -*-
"""Untitled7.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Dx1xko5obV4vSt65snU3PE_1QR-485VS
"""

import pandas as pd

df = pd.read_csv(
    "sideN.csv",
    header=None,
    names = ['AccX', 'AccY', 'AccZ', 'GyrX', 'GyrY', 'GyrZ', 'MagX', 'MagY', 'MagZ']
    )

for col_name in df.columns:
  col = df[col_name]
  col = [float(x.split()[-1]) for x in col]
  df[col_name] = col

new_df = pd.DataFrame()
new_df['X'] = pd.concat([df['AccX'], df['GyrX'], df['MagX']], ignore_index=True)
new_df['Y'] = pd.concat([df['AccY'], df['GyrY'], df['MagY']], ignore_index=True)
new_df['Z'] = pd.concat([df['AccZ'], df['GyrZ'], df['MagZ']], ignore_index=True)

new_df.to_csv('prone.csv')
