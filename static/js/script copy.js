
console.log("script.js loaded");

window.onload = function() {
    // 获取模态框和相关元素
    const resetPasswordModal = document.getElementById('resetPasswordModal');
    console.log('resetPasswordModal:', resetPasswordModal);
    const forgotPasswordLink = document.getElementById('forgotPasswordLink');
    console.log('forgotPasswordLink:', forgotPasswordLink);
    const resetPasswordBtn = document.getElementById('resetPasswordBtn');
    console.log('resetPasswordBtn:', resetPasswordBtn);

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
      // 在这里发送 AJAX 请求到服务器进行密码重置
      console.log('用户名:', username);
      // ...
    });
};

  