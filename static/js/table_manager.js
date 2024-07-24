document.addEventListener('DOMContentLoaded', () => {
    const sampleTable = document.getElementById('sampleTable');
    const addRowBtn = document.getElementById('addRowBtn');
    const addColumnBtn = document.getElementById('addColumnBtn');
    const deleteRowBtn = document.getElementById('deleteRowBtn');
    const saveBtn = document.getElementById('saveBtn');
    const selectAllCheckbox = document.getElementById('selectAll');

    // 添加行
    addRowBtn.onclick = function() {
        const newRow = sampleTable.insertRow();
        newRow.innerHTML = `<td><input type="checkbox" class="rowCheckbox"></td>`;
        for (let i = 1; i < sampleTable.rows[0].cells.length - 1; i++) {
            const newCell = newRow.insertCell();
            newCell.contentEditable = "true";
        }
    };

    // 添加列
    addColumnBtn.onclick = function() {
        const headerRow = sampleTable.rows[0];
        const newHeaderCell = headerRow.insertCell(headerRow.cells.length - 1);
        newHeaderCell.contentEditable = "true";
        newHeaderCell.innerText = "新列";

        for (let i = 1; i < sampleTable.rows.length; i++) {
            const row = sampleTable.rows[i];
            const newCell = row.insertCell(row.cells.length);
            newCell.contentEditable = "true";
        }
    };

    // 删除选中行
    deleteRowBtn.onclick = function() {
        const checkboxes = document.querySelectorAll('.rowCheckbox:checked');
        checkboxes.forEach(checkbox => {
            const row = checkbox.closest('tr');
            sampleTable.deleteRow(row.rowIndex);
        });
    };

    // 全选/取消全选
    selectAllCheckbox.onclick = function() {
        const checkboxes = document.querySelectorAll('.rowCheckbox');
        checkboxes.forEach(checkbox => {
            checkbox.checked = selectAllCheckbox.checked;
        });
    };

    // 保存数据
    saveBtn.onclick = function() {
        const tableData = [];
        const rows = sampleTable.rows;

        // 获取表格数据
        for (let i = 1; i < rows.length; i++) { // 跳过表头
            const row = rows[i];
            const rowData = {};
            for (let j = 1; j < row.cells.length - 1; j++) { // 跳过第一个复选框列和最后一个操作列
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