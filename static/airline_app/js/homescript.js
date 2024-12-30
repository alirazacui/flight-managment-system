document.addEventListener('DOMContentLoaded', () => { 
    const customerBtn = document.getElementById('customer-btn');
    const adminBtn = document.getElementById('admin-btn');
    const loginTitle = document.getElementById('login-title');
  
    // Handle button clicks
    customerBtn.addEventListener('click', () => {
      loginTitle.textContent = 'Customer Login';
      customerBtn.classList.add('active');
      adminBtn.classList.remove('active');
    });
  
    adminBtn.addEventListener('click', () => {
      loginTitle.textContent = 'Admin Login';
      adminBtn.classList.add('active');
      customerBtn.classList.remove('active');
    });
  });
  