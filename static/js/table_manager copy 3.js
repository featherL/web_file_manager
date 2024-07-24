console.log("JavaScript file loaded"); // 确认JS文件加载

document.addEventListener('DOMContentLoaded', () => {
    console.log("DOM fully loaded and parsed"); // 确认DOM内容加载完毕

    const sampleTable = document.getElementById('sampleTable');
    const addRowBtn = document.getElementById('addRowBtn');
    const addColumnBtn = document.getElementById('addColumnBtn');
    const saveBtn = document.getElementById('saveBtn');
    const deleteRowsBtn = document.getElementById('deleteRowsBtn'); // 获取删除按钮

    // 添加行
    addRowBtn.onclick = function() {
        console.log("Add Row Button Clicked"); // 调试信息
        const newRow = sampleTable.insertRow();
        const checkboxCell = newRow.insertCell(); // 插入复选框单元格
        checkboxCell.innerHTML = '<input type="checkbox" class="rowCheckbox">';
        for (let i = 0; i < sampleTable.rows[0].cells.length - 2; i++) {
            const newCell = newRow.insertCell();
            newCell.contentEditable = "true";
        }
    };

    // 删除选中行
    deleteRowsBtn.onclick = function() {
        console.log("Delete Rows Button Clicked"); // 调试信息
        const checkboxes = document.querySelectorAll('.rowCheckbox:checked');
        checkboxes.forEach(checkbox => {
            const row = checkbox.parentNode.parentNode;
            sampleTable.deleteRow(row.rowIndex);
        });
    };

    // 添加列
    addColumnBtn.onclick = function() {
        console.log("Add Column Button Clicked"); // 调试信息
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





    // 保存数据
    // saveBtn.onclick = function() {
    //     console.log("Save Button Clicked"); // 调试信息
    //     const tableData = [];
    //     const rows = sampleTable.rows;

    //     // 获取表格数据
    //     for (let i = 1; i < rows.length; i++) { // 跳过表头
    //         const row = rows[i];
    //         const rowData = {};
    //         for (let j = 1; j < row.cells.length - 1; j++) { // 跳过复选框和最后一列
    //             rowData[sampleTable.rows[0].cells[j].innerText] = row.cells[j].innerText;
    //         }
    //         tableData.push(rowData);
    //     }

    //     // 发送数据到后端
    //     fetch('/save_table', {
    //         method: 'POST',
    //         headers: {
    //             'Content-Type': 'application/json',
    //         },
    //         body: JSON.stringify({ data: tableData }),
    //     })
    //     .then(response => response.json())
    //     .then(data => {
    //         if (data.success) {
    //             alert('Data saved successfully!');
    //         } else {
    //             alert('Error saving data.');
    //         }
    //     });
    // };
    saveBtn.onclick = function() {
        console.log("Save Button Clicked"); // 调试信息
        const tableData = [];
        const rows = sampleTable.rows;
    
        // 获取表格数据
        for (let i = 1; i < rows.length; i++) { // 跳过表头
            const row = rows[i];
            const rowData = {};
            for (let j = 1; j < row.cells.length; j++) { // 遍历所有单元格,包括新增的列
                const columnIndex = j; // 列索引从0开始
                const columnName = sampleTable.rows[0].cells[columnIndex].innerText || `新列${columnIndex}`;
                rowData[columnName] = row.cells[j].innerText;
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