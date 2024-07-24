from flask import Flask, request, send_file, render_template
import subprocess
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('stacked_barplot_2.html')

@app.route('/plot', methods=['POST'])
def plot():
    data = request.json['data']
    program = request.json['program']
    image_width = float(request.json['image_width'])
    image_height = float(request.json['image_height'])
    title = request.json['title']
    x_label = request.json['x_label']
    y_label = request.json['y_label']
    show_legend = request.json['show_legend']

    # Save the data to a temporary file
    data_file = 'scripts/temp_data.tsv'
    with open(data_file, 'w') as f:
        f.write(data)

    # Determine which script to run based on the program
    if program == 'stacked_barplot_matplotlib':
        script = 'plot_matplotlib.py'
    elif program == 'stacked_barplot_ggplot':
        script = 'plot_ggplot.R'
    else:
        return 'Invalid program', 400

    # Construct the command to run
    command = []
    if script.endswith('.py'):
        command = ['python', f'scripts/{script}', data_file, str(image_width), str(image_height), title, x_label, y_label, str(show_legend)]
    elif script.endswith('.R'):
        command = ['Rscript', f'scripts/{script}', data_file, str(image_width), str(image_height), title, x_label, y_label, str(show_legend)]

    # Run the script
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        return f"Error running script: {result.stderr}", 500

    return send_file('static/plot.png', mimetype='image/png')



if __name__ == '__main__':
    app.run(host='192.168.6.182', port=9094, debug=True)