import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def show_corr_heatmap(df):
    df_corr = df.corr()
    print(df_corr)

    sns.heatmap(df_corr, annot=True, fmt='.2f', vmax=1, vmin=-1, center=0, cmap='RdYlBu_r')
    plt.show()

def show_scatterplot(df, col_name):
    df.plot(kind="scatter", x="rank", y=col_name)
    plt.show()

def show_scatterplot_matrix(df):
    sns.pairplot(df, hue='type')
    plt.show()

if __name__ == '__main__':
    df = pd.read_csv('./csv/bukken_sparse3.csv')

    df_city = df[df["type"]==0]
    df_stations = df[df["type"]==1]

    show_corr_heatmap(df)
    show_corr_heatmap(df_city)
    show_corr_heatmap(df_stations)

    show_scatterplot_matrix(df)
'''
    show_scatterplot(df_city, "num")
    show_scatterplot(df_city, "distance")
    show_scatterplot(df_city, "tokyo-distance")

    show_scatterplot(df_stations, "sparse")
'''
