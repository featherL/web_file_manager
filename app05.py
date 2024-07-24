from flask import Flask, request, send_file, render_template
import subprocess
import os
import json

app = Flask(__name__)

# app.py：

# 检查和获取所有必要的参数。如果请求中缺少某些参数，则使用默认值。

# 将这些参数打包为一个字典 input_params 并将其以 JSON 格式传递给外部脚本。

# 运行外部脚本时，捕获并返回任何错误信息。



# plot_matplotlib.py 和 plot_ggplot.R：

# 从标准输入读取 JSON 格式的参数。

# 使用从 JSON 中提取的参数进行绘图。

# 将生成的图像保存为 static/plot.png，以便 Flask 应用可以发送给客户端。

@app.route('/')
def index():
    return render_template('stacked_barplot_2.html')

@app.route('/plot', methods=['POST'])
def plot():
    # Extract data from the request
    data = request.json.get('data')
    program = request.json.get('program')
    image_width = float(request.json.get('image_width', 10))
    image_height = float(request.json.get('image_height', 7))
    title = request.json.get('title', 'Stacked Bar Plot')
    x_label = request.json.get('x_label', 'ID')
    y_label = request.json.get('y_label', 'Expression Level')
    show_legend = request.json.get('show_legend', True)
    x_rotation = int(request.json.get('x_rotation', 45))

    # Save the data to a temporary file
    data_file = 'scripts/temp_data.tsv'
    with open(data_file, 'w') as f:
        f.write(data)

    # Construct the command to run
    input_params = {
        'data': data,
        'image_width': image_width,
        'image_height': image_height,
        'title': title,
        'x_label': x_label,
        'y_label': y_label,
        'show_legend': show_legend,
        'x_rotation': x_rotation
    }

    script_dir = 'scripts'
    if program == 'stacked_barplot_matplotlib':
        script = 'stack_plot_v2.py'
        command = ['python', os.path.join(script_dir, script)]
    elif program == 'stacked_barplot_ggplot':
        script = 'stack_plot_v2.R'
        command = ['Rscript', os.path.join(script_dir, script)]
    else:
        return 'Invalid program', 400

    # Run the script with JSON input
    result = subprocess.run(command, input=json.dumps(input_params), text=True, capture_output=True)
    if result.returncode != 0:
        return f"Error running script: {result.stderr}", 500

    return send_file('static/plot.png', mimetype='image/png')

if __name__ == '__main__':
    app.run(host='192.168.6.182', port=9094, debug=True)