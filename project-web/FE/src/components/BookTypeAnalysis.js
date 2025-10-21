import React, { useState, useEffect } from 'react';
import './BookTypeAnalysis.css';

const BookTypeAnalysis = () => {
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchAnalytics();
  }, []);

  const fetchAnalytics = async () => {
    try {
      const response = await fetch('/api/analytics');
      const data = await response.json();
      setAnalytics(data);
    } catch (err) {
      setError('Không thể tải dữ liệu phân tích');
      console.error('Error fetching analytics:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="loading">Đang tải dữ liệu...</div>;
  if (error) return <div className="error">{error}</div>;
  if (!analytics) return <div className="error">Không có dữ liệu</div>;

  const bookTypes = analytics.book_type_analysis || {};

  return (
    <div className="book-type-analysis">
      <h2>📚 Phân Tích Khách Hàng Theo Loại Sách</h2>
      
      <div className="summary-cards">
        <div className="card">
          <h3>Tổng Khách Hàng</h3>
          <p className="number">{analytics.summary?.total_customers || 0}</p>
        </div>
        <div className="card">
          <h3>Khách Hàng Tiềm Năng</h3>
          <p className="number">{analytics.summary?.potential_customers || 0}</p>
          <p className="percentage">{analytics.summary?.potential_percentage?.toFixed(1)}%</p>
        </div>
        <div className="card">
          <h3>Tuổi Trung Bình</h3>
          <p className="number">{analytics.summary?.average_age?.toFixed(1)}</p>
        </div>
        <div className="card">
          <h3>Chi Tiêu TB</h3>
          <p className="number">{analytics.summary?.average_spending?.toLocaleString()} VNĐ</p>
        </div>
      </div>

      <div className="book-types-section">
        <h3>🏆 Top Loại Sách Được Yêu Thích</h3>
        <div className="book-types-grid">
          {Object.entries(bookTypes)
            .sort(([,a], [,b]) => b.customers - a.customers)
            .slice(0, 8)
            .map(([bookType, stats]) => (
              <div key={bookType} className="book-type-card">
                <h4>{bookType}</h4>
                <div className="stats">
                  <div className="stat">
                    <span className="label">Khách hàng:</span>
                    <span className="value">{stats.customers}</span>
                    <span className="percentage">({stats.percentage.toFixed(1)}%)</span>
                  </div>
                  <div className="stat">
                    <span className="label">Tổng sách:</span>
                    <span className="value">{stats.total_books}</span>
                  </div>
                  <div className="stat">
                    <span className="label">TB/khách hàng:</span>
                    <span className="value">{stats.avg_books_per_customer.toFixed(1)}</span>
                  </div>
                </div>
                <div className="progress-bar">
                  <div 
                    className="progress" 
                    style={{ width: `${stats.percentage}%` }}
                  ></div>
                </div>
              </div>
            ))}
        </div>
      </div>

      <div className="visualization-section">
        <h3>📊 Biểu Đồ Phân Tích</h3>
        <div className="chart-container">
          <img 
            src="/images/book_type_analysis.png" 
            alt="Phân tích theo loại sách"
            className="analysis-chart"
          />
        </div>
      </div>

      <div className="insights-section">
        <h3>💡 Insights Chính</h3>
        <div className="insights-grid">
          <div className="insight-card">
            <h4>🔥 Loại Sách Hot Nhất</h4>
            <p>
              {Object.entries(bookTypes)
                .sort(([,a], [,b]) => b.customers - a.customers)[0]?.[0] || 'N/A'}
            </p>
          </div>
          <div className="insight-card">
            <h4>📈 Tỷ Lệ Tiềm Năng</h4>
            <p>{analytics.summary?.potential_percentage?.toFixed(1)}% khách hàng có tiềm năng</p>
          </div>
          <div className="insight-card">
            <h4>💰 Chi Tiêu Trung Bình</h4>
            <p>{analytics.summary?.average_spending?.toLocaleString()} VNĐ/khách hàng</p>
          </div>
          <div className="insight-card">
            <h4>🎯 Độ Tuổi Chính</h4>
            <p>{analytics.summary?.average_age?.toFixed(1)} tuổi (sinh viên)</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default BookTypeAnalysis;
