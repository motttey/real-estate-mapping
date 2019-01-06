import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def show_corr_heatmap(df):
    df_corr = df.corr()
    print(df_corr)

    sns.heatmap(df_corr, vmax=1, vmin=-1, center=0)
    plt.show()

if __name__ == '__main__':
    df = pd.read_csv('bukken_sparse3.csv')

    df_city = df[df["type"]==0]
    df_stations = df[df["type"]==1]

    show_corr_heatmap(df)
    show_corr_heatmap(df_city)
    show_corr_heatmap(df_stations)
