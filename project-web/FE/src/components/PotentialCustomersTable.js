import React, { useState, useEffect } from 'react';
import './PotentialCustomersTable.css';

const PotentialCustomersTable = () => {
  const [customers, setCustomers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [stats, setStats] = useState({});
  const [filter, setFilter] = useState('all');

  useEffect(() => {
    fetchPotentialCustomers();
  }, []);

  const fetchPotentialCustomers = async () => {
    try {
      setLoading(true);
      const response = await fetch('http://localhost:5001/api/potential-customers');
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      
      // Backend trả về array trực tiếp
      if (Array.isArray(data)) {
        setCustomers(data);
        
        // Tính toán stats từ data
        const highPotential = data.filter(c => c.probability >= 0.7).length;
        const mediumPotential = data.filter(c => c.probability >= 0.4 && c.probability < 0.7).length;
        const lowPotential = data.filter(c => c.probability < 0.4).length;
        const avgProbability = data.reduce((sum, c) => sum + c.probability, 0) / data.length;
        const avgActions = data.reduce((sum, c) => sum + c.total_actions, 0) / data.length;
        const avgSpending = data.reduce((sum, c) => sum + c.total_spending, 0) / data.length;
        
        setStats({
          total: data.length,
          high: highPotential,
          medium: mediumPotential,
          low: lowPotential,
          avgProbability: avgProbability,
          avgActions: Math.round(avgActions),
          avgSpending: Math.round(avgSpending)
        });
      } else if (data.error) {
        setError(data.error);
      } else {
        setError('Invalid data format');
      }
    } catch (err) {
      setError(`Error connecting to server: ${err.message}`);
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  const filteredCustomers = customers.filter(customer => {
    if (filter === 'all') return true;
    
    // Tính potential dựa trên probability
    let potential = 'low';
    if (customer.probability >= 0.7) potential = 'high';
    else if (customer.probability >= 0.4) potential = 'medium';
    
    return potential === filter;
  });

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('vi-VN', {
      style: 'currency',
      currency: 'VND'
    }).format(amount);
  };

  const getPotentialBadgeClass = (potential) => {
    switch (potential.toLowerCase()) {
      case 'high': return 'badge-high';
      case 'medium': return 'badge-medium';
      case 'low': return 'badge-low';
      default: return 'badge-default';
    }
  };

  if (loading) {
    return (
      <div className="loading-container">
        <div className="loading-spinner"></div>
        <p>Đang tải dữ liệu khách hàng tiềm năng...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="error-container">
        <h3>Lỗi tải dữ liệu</h3>
        <p>{error}</p>
        <button onClick={fetchPotentialCustomers} className="retry-btn">
          Thử lại
        </button>
      </div>
    );
  }

  return (
    <div className="potential-customers-container">
      <div className="header">
        <h2>🎯 Danh Sách Khách Hàng Tiềm Năng</h2>
        <p>Hệ thống dự đoán khách hàng tiềm năng - Dataset 576 sinh viên</p>
      </div>

      {/* Thống kê tổng quan */}
      <div className="stats-grid">
        <div className="stat-card">
          <h3>{stats.total}</h3>
          <p>Tổng khách hàng</p>
        </div>
        <div className="stat-card high">
          <h3>{stats.high}</h3>
          <p>Tiềm năng cao</p>
        </div>
        <div className="stat-card medium">
          <h3>{stats.medium}</h3>
          <p>Tiềm năng trung bình</p>
        </div>
        <div className="stat-card">
          <h3>{(stats.avgProbability * 100).toFixed(1)}%</h3>
          <p>Xác suất TB</p>
        </div>
        <div className="stat-card">
          <h3>{stats.avgActions}</h3>
          <p>Hành động TB</p>
        </div>
        <div className="stat-card">
          <h3>{formatCurrency(stats.avgSpending)}</h3>
          <p>Chi tiêu TB</p>
        </div>
      </div>

      {/* Bộ lọc */}
      <div className="filter-section">
        <label>Lọc theo tiềm năng:</label>
        <select 
          value={filter} 
          onChange={(e) => setFilter(e.target.value)}
          className="filter-select"
        >
          <option value="all">Tất cả</option>
          <option value="high">Tiềm năng cao</option>
          <option value="medium">Tiềm năng trung bình</option>
          <option value="low">Tiềm năng thấp</option>
        </select>
        <span className="filter-count">
          Hiển thị {filteredCustomers.length} / {customers.length} khách hàng
        </span>
      </div>

      {/* Bảng dữ liệu */}
      <div className="table-container">
        <table className="customers-table">
          <thead>
            <tr>
              <th>STT</th>
              <th>Tên</th>
              <th>Email</th>
              <th>Tuổi</th>
              <th>Hành động</th>
              <th>Chi tiêu</th>
              <th>Tiềm năng</th>
              <th>Xác suất</th>
            </tr>
          </thead>
          <tbody>
            {filteredCustomers.map((customer, index) => {
              // Tính potential dựa trên probability
              let potential = 'Low';
              if (customer.probability >= 0.7) potential = 'High';
              else if (customer.probability >= 0.4) potential = 'Medium';
              
              return (
                <tr key={customer.id}>
                  <td>{index + 1}</td>
                  <td className="customer-name">{customer.name}</td>
                  <td className="customer-email">{customer.email}</td>
                  <td>{customer.age}</td>
                  <td>{customer.total_actions}</td>
                  <td className="spending">{formatCurrency(customer.total_spending)}</td>
                  <td>
                    <span className={`badge ${getPotentialBadgeClass(potential)}`}>
                      {potential}
                    </span>
                  </td>
                  <td className="probability">
                    {(customer.probability * 100).toFixed(1)}%
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      {/* Chú thích */}
      <div className="legend">
        <h4>📋 Chú thích:</h4>
        <ul>
          <li><strong>Tên:</strong> Tên khách hàng</li>
          <li><strong>Email:</strong> Email liên hệ</li>
          <li><strong>Hành động:</strong> Tổng số hành động (view, purchase)</li>
          <li><strong>Chi tiêu:</strong> Tổng chi tiêu (VNĐ)</li>
          <li><strong>Tiềm năng:</strong> High (≥70%), Medium (40-70%), Low (&lt;40%)</li>
          <li><strong>Xác suất:</strong> Xác suất dự đoán từ mô hình ML</li>
        </ul>
      </div>
    </div>
  );
};

export default PotentialCustomersTable;
