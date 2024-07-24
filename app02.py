from flask import Flask, request, send_file, render_template_string
import io
import pandas as pd
import matplotlib.pyplot as plt

app = Flask(__name__)

@app.route('/')
def index():
    return render_template_string('''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
<td valign="top" align="center">
<p>
Program
<select name="PROGRAM" id="program">
<option selected="">stacked_barplot</option>
</select><br>
Please choose suitable format and paste your data matrix below (tab separated text file) <u>long_data_matrix</u> format<br>
<textarea name="long_data_matrix" id="long_data_matrix" rows="8" cols="60"></textarea>
<br>
Or load it from disk
<input name="SEQFILE" type="file" id="file_input">
<br>
<input name="button" type="button" onclick="clearData()" value="Clear long_data_matrix">
<input name="submit" type="button" value="Run PLOT" onclick="plotData()">
</p>
<p>
<img id="plot" src="" alt="Plot will be displayed here">
</td>
<script>
function clearData() {
    document.getElementById('long_data_matrix').value = '';
    document.getElementById('file_input').value = '';
}

function plotData() {
    var data = document.getElementById('long_data_matrix').value;
    var program = document.getElementById('program').value;
    
    fetch('/plot', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({data: data, program: program})
    })
    .then(response => response.blob())
    .then(blob => {
        var url = URL.createObjectURL(blob);
        document.getElementById('plot').src = url;
    });
}

document.getElementById('file_input').addEventListener('change', function(event) {
    var file = event.target.files[0];
    var reader = new FileReader();
    reader.onload = function(event) {
        document.getElementById('long_data_matrix').value = event.target.result;
    };
    reader.readAsText(file);
});
</script>
</body>
</html>
''')

@app.route('/plot', methods=['POST'])
def plot():
    data = request.json['data']
    program = request.json['program']
    
    # Convert the data to a pandas DataFrame
    df = pd.read_csv(io.StringIO(data), sep='\t')
    
    if program == 'stacked_barplot':
        # Create the stacked bar plot
        df_pivot = df.pivot(index='ID', columns='Gene', values='Expr')
        df_pivot.plot(kind='bar', stacked=True)
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