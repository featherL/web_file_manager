from flask import Flask, request, send_file, render_template_string,render_template
import io
import pandas as pd
import matplotlib.pyplot as plt

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('stacked_barplot.html')

@app.route('/plot', methods=['POST'])
def plot():
    data = request.json['data']
    program = request.json['program']
    image_width = float(request.json['image_width'])
    image_height = float(request.json['image_height'])
    
    # Convert the data to a pandas DataFrame
    df = pd.read_csv(io.StringIO(data), sep='\t')
    
    if program == 'stacked_barplot':
        # Create the stacked bar plot
        df_pivot = df.pivot(index='ID', columns='Gene', values='Expr')
        df_pivot.plot(kind='bar', stacked=True, figsize=(image_width/2.54, image_height/2.54))  # convert cm to inches
        plt.xlabel('ID')
        plt.ylabel('Expression Level')
        plt.title('Stacked Bar Plot')
        plt.legend(title='Gene', bbox_to_anchor=(1.05, 1), loc='upper left')

    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    
    return send_file(img, mimetype='image/png')


if __name__ == '__main__':
    app.run(host='192.168.6.182', port=9094, debug=True)