import pandas as pd
import matplotlib.pyplot as plt
import io
import sys
import json

def plot_stacked_barplot_matplotlib(data, image_width, image_height, title, x_label, y_label, show_legend, x_rotation):
    # Convert the data to a pandas DataFrame
    df = pd.read_csv(io.StringIO(data), sep='\t')
    
    # Create the stacked bar plot
    df_pivot = df.pivot(index='ID', columns='Gene', values='Expr')
    ax = df_pivot.plot(kind='bar', stacked=True, figsize=(image_width / 2.54, image_height / 2.54))  # convert cm to inches
    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.legend(title='Gene' if show_legend else None, bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.xticks(rotation=x_rotation)
    
    # Save the plot to a BytesIO object
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    
    return img

if __name__ == "__main__":
    input_json = json.load(sys.stdin)
    data = input_json['data']
    image_width = float(input_json['image_width'])
    image_height = float(input_json['image_height'])
    title = input_json['title']
    x_label = input_json['x_label']
    y_label = input_json['y_label']
    show_legend = input_json['show_legend']
    x_rotation = int(input_json['x_rotation'])
    
    img = plot_stacked_barplot_matplotlib(data, image_width, image_height, title, x_label, y_label, show_legend, x_rotation)
    with open('static/plot.png', 'wb') as f:
        f.write(img.read())