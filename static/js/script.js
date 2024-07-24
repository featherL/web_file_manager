console.log("script.js loaded");

window.onload = function() {
    // 获取模态框和相关元素
    const resetPasswordModal = document.getElementById('resetPasswordModal');
    const forgotPasswordLink = document.getElementById('forgotPasswordLink');
    const resetPasswordBtn = document.getElementById('resetPasswordBtn');

    // 显示模态框
    function showResetPasswordModal() {
        resetPasswordModal.style.display = 'block';
    }

    // 隐藏模态框
    function hideResetPasswordModal() {
        resetPasswordModal.style.display = 'none';
    }

    // 点击"忘记密码"链接时显示模态框
    forgotPasswordLink.addEventListener('click', function(event) {
        event.preventDefault(); // 防止链接默认行为
        showResetPasswordModal();
    });

    // 点击模态框外部区域时隐藏模态框
    window.addEventListener('click', function(event) {
        if (event.target == resetPasswordModal) {
            hideResetPasswordModal();
        }
    });

    // 处理"找回密码"按钮点击事件
    resetPasswordBtn.addEventListener('click', function() {
        const username = document.getElementById('username').value;

        // 隐藏旧的模态框
        hideResetPasswordModal();

        // 发送 AJAX 请求到后端验证用户名
        fetch('/reset_password', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: 'username=' + encodeURIComponent(username)
        })
        .then(response => {
            if (response.ok) {
                return response.text();
            } else {
                throw new Error('用户名不存在');
            }
        })
        .then(html => {
            const modal = document.createElement('div');
            modal.innerHTML = html;
            modal.style.zIndex = '9999'; // 设置较高的 z-index 值
            modal.style.position = 'fixed'; // 设置为固定定位
            modal.style.top = '50%'; // 垂直居中
            modal.style.left = '50%'; // 水平居中
            modal.style.transform = 'translate(-50%, -50%)'; // 调整位置
            document.body.appendChild(modal);
            $(modal).modal('show');
        })
        .catch(error => {
            alert(error.message);
        });
    });
};

  