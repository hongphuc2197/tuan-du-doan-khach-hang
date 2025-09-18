import React, { useState } from 'react';
import axios from 'axios';

const PredictionForm = () => {
  const [formData, setFormData] = useState({
    Income: '',
    Kidhome: '',
    Teenhome: '',
    Recency: '',
    MntWines: '',
    MntFruits: '',
    MntMeatProducts: '',
    MntFishProducts: '',
    MntSweetProducts: '',
    MntGoldProds: '',
    NumDealsPurchases: '',
    NumWebPurchases: '',
    NumCatalogPurchases: '',
    NumStorePurchases: '',
    NumWebVisitsMonth: '',
  });

  const [prediction, setPrediction] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    
    try {
      const response = await axios.post('http://localhost:3001/api/predict', formData);
      setPrediction(response.data);
    } catch (err) {
      setError(err.response?.data?.error || 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="prediction-form">
      <h2>Dự đoán khách hàng tiềm năng mua sách công nghệ giáo dục</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Thu nhập (VND):</label>
          <input
            type="number"
            name="Income"
            value={formData.Income}
            onChange={handleChange}
            placeholder="Nhập thu nhập hàng tháng"
            required
          />
        </div>

        <div className="form-group">
          <label>Số con nhỏ:</label>
          <input
            type="number"
            name="Kidhome"
            value={formData.Kidhome}
            onChange={handleChange}
            min="0"
            max="5"
            required
          />
        </div>

        <div className="form-group">
          <label>Số con tuổi teen:</label>
          <input
            type="number"
            name="Teenhome"
            value={formData.Teenhome}
            onChange={handleChange}
            min="0"
            max="5"
            required
          />
        </div>

        <div className="form-group">
          <label>Số ngày từ lần mua cuối:</label>
          <input
            type="number"
            name="Recency"
            value={formData.Recency}
            onChange={handleChange}
            placeholder="Số ngày kể từ lần mua sách cuối"
            required
          />
        </div>

        <div className="form-group">
          <label>Chi tiêu cho sách Công nghệ giáo dục (VND):</label>
          <input
            type="number"
            name="MntWines"
            value={formData.MntWines}
            onChange={handleChange}
            placeholder="Ví dụ: 150000"
            required
          />
        </div>

        <div className="form-group">
          <label>Chi tiêu cho sách Phương pháp giảng dạy (VND):</label>
          <input
            type="number"
            name="MntFruits"
            value={formData.MntFruits}
            onChange={handleChange}
            placeholder="Ví dụ: 180000"
            required
          />
        </div>

        <div className="form-group">
          <label>Chi tiêu cho sách Công nghệ thông tin (VND):</label>
          <input
            type="number"
            name="MntMeatProducts"
            value={formData.MntMeatProducts}
            onChange={handleChange}
            placeholder="Ví dụ: 120000"
            required
          />
        </div>

        <div className="form-group">
          <label>Chi tiêu cho sách Thiết kế web (VND):</label>
          <input
            type="number"
            name="MntFishProducts"
            value={formData.MntFishProducts}
            onChange={handleChange}
            placeholder="Ví dụ: 95000"
            required
          />
        </div>

        <div className="form-group">
          <label>Chi tiêu cho sách Lập trình (VND):</label>
          <input
            type="number"
            name="MntSweetProducts"
            value={formData.MntSweetProducts}
            onChange={handleChange}
            placeholder="Ví dụ: 130000"
            required
          />
        </div>

        <div className="form-group">
          <label>Chi tiêu cho sách Nghiên cứu khoa học (VND):</label>
          <input
            type="number"
            name="MntGoldProds"
            value={formData.MntGoldProds}
            onChange={handleChange}
            placeholder="Ví dụ: 140000"
            required
          />
        </div>

        <div className="form-group">
          <label>Số lần mua hàng giảm giá:</label>
          <input
            type="number"
            name="NumDealsPurchases"
            value={formData.NumDealsPurchases}
            onChange={handleChange}
            min="0"
            required
          />
        </div>

        <div className="form-group">
          <label>Số lần mua sách online:</label>
          <input
            type="number"
            name="NumWebPurchases"
            value={formData.NumWebPurchases}
            onChange={handleChange}
            min="0"
            required
          />
        </div>

        <div className="form-group">
          <label>Số lần mua sách qua catalog:</label>
          <input
            type="number"
            name="NumCatalogPurchases"
            value={formData.NumCatalogPurchases}
            onChange={handleChange}
            min="0"
            required
          />
        </div>

        <div className="form-group">
          <label>Số lần mua sách tại cửa hàng:</label>
          <input
            type="number"
            name="NumStorePurchases"
            value={formData.NumStorePurchases}
            onChange={handleChange}
            min="0"
            required
          />
        </div>

        <div className="form-group">
          <label>Số lần truy cập website trong tháng:</label>
          <input
            type="number"
            name="NumWebVisitsMonth"
            value={formData.NumWebVisitsMonth}
            onChange={handleChange}
            min="0"
            required
          />
        </div>

        <button type="submit" disabled={loading}>
          {loading ? 'Đang dự đoán...' : 'Dự đoán khách hàng tiềm năng'}
        </button>
      </form>

      {error && (
        <div className="error-message">
          {error}
        </div>
      )}

      {prediction && (
        <div className="prediction-result">
          <h3>Kết quả dự đoán:</h3>
          <p>
            Khách hàng này được dự đoán là: 
            <strong>{prediction.result === 1 ? ' Khách hàng tiềm năng mua sách' : ' Không phải khách hàng tiềm năng'}</strong>
          </p>
          {prediction.probability && (
            <p>Độ tin cậy: {(prediction.probability * 100).toFixed(2)}%</p>
          )}
          {prediction.result === 1 ? (
            <div className="recommendations">
              <h4>Đề xuất marketing:</h4>
              <ul>
                <li>Gửi thông báo về sách mới về AI và công nghệ giáo dục</li>
                <li>Cung cấp ưu đãi đặc biệt cho giáo viên và sinh viên</li>
                <li>Tạo danh sách sách gợi ý theo chuyên ngành</li>
                <li>Mời tham gia hội thảo và workshop về công nghệ giáo dục</li>
              </ul>
            </div>
          ) : (
            <div className="recommendations">
              <h4>Đề xuất marketing:</h4>
              <ul>
                <li>Gửi email giới thiệu các sách bestseller về lập trình</li>
                <li>Cung cấp mã giảm giá 20% cho lần mua đầu tiên</li>
                <li>Tạo nội dung về lợi ích của việc học công nghệ thông tin</li>
                <li>Gửi sample chapters miễn phí để khuyến khích mua sách</li>
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default PredictionForm; 