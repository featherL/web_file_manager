document.addEventListener('DOMContentLoaded', () => {
    const sampleTable = document.getElementById('sampleTable');
    const addRowBtn = document.getElementById('addRowBtn');
    const saveBtn = document.getElementById('saveBtn');

    // 添加行
    addRowBtn.onclick = function() {
        const newRow = sampleTable.insertRow();
        for (let i = 0; i < sampleTable.rows[0].cells.length - 1; i++) {
            const newCell = newRow.insertCell();
            newCell.contentEditable = "true";
        }
        const actionCell = newRow.insertCell();
        actionCell.innerHTML = '<button class="deleteRowBtn">删除</button>';
    };

    // 删除行
    sampleTable.addEventListener('click', function(event) {
        if (event.target.classList.contains('deleteRowBtn')) {
            const row = event.target.closest('tr');
            sampleTable.deleteRow(row.rowIndex);
        }
    });

    // 保存数据
    saveBtn.onclick = function() {
        const tableData = [];
        const rows = sampleTable.rows;

        // 获取表格数据
        for (let i = 1; i < rows.length; i++) { // 跳过表头
            const row = rows[i];
            const rowData = {};
            for (let j = 0; j < row.cells.length - 1; j++) { // 跳过最后一个操作列
                rowData[sampleTable.rows[0].cells[j].innerText] = row.cells[j].innerText;
            }
            tableData.push(rowData);
        }

        // 发送数据到后端
        fetch('/save_table', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ data: tableData }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Data saved successfully!');
            } else {
                alert('Error saving data.');
            }
        });
    };
});