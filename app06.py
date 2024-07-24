from flask import Flask, request, send_file, render_template
import subprocess
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
    

@app.route('/tools/<tool>')
def tool_page(tool):
    if tool == 'stacked_barplot':
        return render_template('stacked_barplot.html')
    elif tool == 'boxplot':
        return render_template('boxplot.html')
    elif tool == 'heatmap':
        return render_template('heatmap.html')
    else:
        return 'Tool not found', 404

@app.route('/plot/<tool>', methods=['POST'])
def plot(tool):
    print("tool name=====>",tool)
    if tool == 'stacked_barplot':
        return stacked_barplot()
    elif tool == 'boxplot':
        return boxplot()
    elif tool == 'heatmap':
        return heatmap()
    else:
        return 'Invalid tool', 400

def stacked_barplot():
    print("run stacked_barplot")
    data = request.json['data']
    print(f"Received data: {data[:100]}...")  # 仅打印前100个字符
    image_width = float(request.json['image_width'])
    image_height = float(request.json['image_height'])
    title = request.json['title']
    x_label = request.json['x_label']
    y_label = request.json['y_label']
    show_legend = request.json['show_legend']
    x_rotation = int(request.json['x_rotation'])

    data_file = 'scripts/temp_data.tsv'
    with open(data_file, 'w') as f:
        f.write(data)

    command = ['Rscript', 'scripts/plot_stacked_barplot.R', data_file, str(image_width), str(image_height), title, x_label, y_label, str(show_legend), str(x_rotation)]
    #command = ['python', 'scripts/plot_matplotlib.py', data_file, str(image_width), str(image_height), title, x_label, y_label, str(show_legend), str(x_rotation)]
    result = subprocess.run(command, capture_output=True, text=True)
    print(f"Command executed with return code {result.returncode}")
    if result.returncode != 0:
        return f"Error running script: {result.stderr}", 500

    return send_file('static/plot.png', mimetype='image/png')

def boxplot():
    data = request.json['data']
    image_width = float(request.json['image_width'])
    image_height = float(request.json['image_height'])
    title = request.json['title']
    x_label = request.json['x_label']
    y_label = request.json['y_label']
    show_legend = request.json['show_legend']
    x_rotation = int(request.json['x_rotation'])

    data_file = 'scripts/temp_data.tsv'
    with open(data_file, 'w') as f:
        f.write(data)

    command = ['Rscript', 'scripts/plot_boxplot.R', data_file, str(image_width), str(image_height), title, x_label, y_label, str(show_legend), str(x_rotation)]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        return f"Error running script: {result.stderr}", 500

    return send_file('static/plot.png', mimetype='image/png')


def heatmap():
    print("run heatmap")
    data = request.json['data']
    image_width = float(request.json['image_width'])
    image_height = float(request.json['image_height'])
    title = request.json['title']
    x_label = request.json['x_label']
    y_label = request.json['y_label']
    show_legend = request.json['show_legend']
    x_rotation = int(request.json['x_rotation'])

    data_file = 'scripts/temp_data.tsv'
    with open(data_file, 'w') as f:
        f.write(data)

    command = ['Rscript', 'scripts/plot_heatmap.R', data_file, str(image_width), str(image_height), title, x_label, y_label, str(show_legend), str(x_rotation)]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        return f"Error running script: {result.stderr}", 500

    return send_file('static/plot.png', mimetype='image/png')

if __name__ == '__main__':
    app.run(host='192.168.6.182', port=9094, debug=True)