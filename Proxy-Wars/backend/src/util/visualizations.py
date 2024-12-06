import matplotlib.pyplot as plt
import seaborn as sns  # Optional, for better visuals
import pandas as pd
import io

'''
Creates a heatmap of the given dataframe and returns it in an io byte buffer
df = dataframe to make heatmap of
title = title of plot
cmap = seaborn color map
vmin = lower bound of the color map values
vmax = upper bound of the color map values
sizeX = the width of the heatmap
sizeY = the height of the heatmap
'''
def createHeatMap(df, title, cmap='viridis',vmin=0,vmax=1, sizeX=12, sizeY=10):
    plt.figure(figsize=(sizeX, sizeY))
    sns.heatmap(df, annot=True, vmin=vmin, vmax=vmax, cmap=cmap) 
    plt.title(title)
    plt.xlabel("Columns")
    plt.ylabel("Index")

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    return buffer