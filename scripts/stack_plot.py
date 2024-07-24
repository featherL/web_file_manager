import sys
import pandas as pd
import matplotlib.pyplot as plt

def plot(data_file, image_width, image_height):
    df = pd.read_csv(data_file, sep='\t')
    df_pivot = df.pivot(index='ID', columns='Gene', values='Expr')
    df_pivot.plot(kind='bar', stacked=True, figsize=(image_width/2.54, image_height/2.54))  # convert cm to inches
    plt.xlabel('ID')
    plt.ylabel('Expression Level')
    plt.title('Stacked Bar Plot')
    plt.legend(title='Gene', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.savefig('static/plot.png', bbox_inches='tight')

if __name__ == '__main__':
    plot(sys.argv[1], float(sys.argv[2]), float(sys.argv[3]))