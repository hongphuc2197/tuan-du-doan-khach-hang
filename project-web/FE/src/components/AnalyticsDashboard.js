import React, { useState, useEffect } from 'react';
import {
  Paper,
  Grid,
  Typography,
  Box,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
} from '@mui/material';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  PointElement,
  LineElement,
} from 'chart.js';
import { Pie, Bar } from 'react-chartjs-2';
// import { getAnalytics } from '../services/customerService';
import { mockAnalytics } from '../data/mockData';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  PointElement,
  LineElement
);

const AnalyticsDashboard = () => {
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchAnalytics = async () => {
      try {
        // Sử dụng dữ liệu mẫu thay vì gọi API
        setAnalytics(mockAnalytics);
        setLoading(false);
      } catch (err) {
        setError('Không thể tải dữ liệu phân tích');
        setLoading(false);
      }
    };

    fetchAnalytics();
  }, []);

  if (loading) return <Typography>Đang tải dữ liệu phân tích...</Typography>;
  if (error) return <Typography color="error">{error}</Typography>;
  if (!analytics) return null;

  // 1. Biểu đồ phân phối phân lớp khách hàng
  const customerDistributionData = {
    labels: ['Sinh viên tiềm năng mua sách', 'Sinh viên không tiềm năng'],
    datasets: [
      {
        data: [analytics.potentialCustomers, analytics.nonPotentialCustomers],
        backgroundColor: ['#4CAF50', '#F44336'],
      },
    ],
  };

  // 2. Phân khúc độ tuổi
  const ageSegmentsData = {
    labels: analytics.demographics.ageSegments.map(s => s.name),
    datasets: [
      {
        data: analytics.demographics.ageSegments.map(s => s.count),
        backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF'],
      },
    ],
  };

  // 3. Phân tích trình độ học vấn
  const educationData = {
    labels: analytics.demographics.education.map(e => e.Education),
    datasets: [
      {
        label: 'Tỷ lệ khách hàng tiềm năng (%)',
        data: analytics.demographics.education.map(e => e.potential_rate),
        backgroundColor: '#4CAF50',
      },
    ],
  };

  // 4. Phân tích thu nhập
  const incomeData = {
    labels: analytics.demographics.income.map(i => i.Income),
    datasets: [
      {
        label: 'Tỷ lệ khách hàng tiềm năng (%)',
        data: analytics.demographics.income.map(i => i.potential_rate),
        backgroundColor: '#2196F3',
      },
    ],
  };

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        Phân tích dữ liệu sinh viên mua sách công nghệ giáo dục
      </Typography>

      <Grid container spacing={3}>
        {/* 1. Phân phối phân lớp khách hàng */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Phân phối phân lớp khách hàng
            </Typography>
            <Box sx={{ height: 300 }}>
              <Pie data={customerDistributionData} />
            </Box>
          </Paper>
        </Grid>

        {/* 2. Phân khúc độ tuổi */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Phân khúc độ tuổi
            </Typography>
            <Box sx={{ height: 300 }}>
              <Pie data={ageSegmentsData} />
            </Box>
          </Paper>
        </Grid>

        {/* 3. Phân tích trình độ học vấn */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Phân tích theo trình độ học vấn
            </Typography>
            <Box sx={{ height: 300 }}>
              <Bar
                data={educationData}
                options={{
                  scales: {
                    y: {
                      beginAtZero: true,
                      title: {
                        display: true,
                        text: 'Tỷ lệ khách hàng tiềm năng (%)'
                      }
                    }
                  }
                }}
              />
            </Box>
          </Paper>
        </Grid>

        {/* 4. Phân tích thu nhập */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Phân tích theo thu nhập
            </Typography>
            <Box sx={{ height: 300 }}>
              <Bar
                data={incomeData}
                options={{
                  scales: {
                    y: {
                      beginAtZero: true,
                      title: {
                        display: true,
                        text: 'Tỷ lệ khách hàng tiềm năng (%)'
                      }
                    }
                  }
                }}
              />
            </Box>
          </Paper>
        </Grid>

        {/* 5. Thống kê chi tiêu theo danh mục sách */}
        <Grid item xs={12}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Thống kê chi tiêu theo danh mục sách công nghệ giáo dục
            </Typography>
            <TableContainer>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>Danh mục sách</TableCell>
                    <TableCell align="right">Trung bình (VND)</TableCell>
                    <TableCell align="right">Trung vị (VND)</TableCell>
                    <TableCell align="right">Tối đa (VND)</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {[
                    { name: 'Công nghệ giáo dục', value: 150000 },
                    { name: 'Phương pháp giảng dạy', value: 180000 },
                    { name: 'Công nghệ thông tin', value: 120000 },
                    { name: 'Thiết kế web', value: 95000 },
                    { name: 'Lập trình', value: 130000 },
                    { name: 'Nghiên cứu khoa học', value: 140000 },
                    { name: 'Giáo dục STEM', value: 160000 },
                    { name: 'Thiết kế UI/UX', value: 170000 },
                    { name: 'Cơ sở dữ liệu', value: 145000 },
                    { name: 'Phát triển ứng dụng', value: 190000 }
                  ].map((book) => (
                    <TableRow key={book.name}>
                      <TableCell>{book.name}</TableCell>
                      <TableCell align="right">{book.value.toLocaleString()}</TableCell>
                      <TableCell align="right">{Math.round(book.value * 0.8).toLocaleString()}</TableCell>
                      <TableCell align="right">{Math.round(book.value * 1.5).toLocaleString()}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </Paper>
        </Grid>

        {/* 6. Thống kê hành vi người dùng trên website */}
        <Grid item xs={12}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Thống kê hành vi người dùng trên website (2 tuần thu thập)
            </Typography>
            <TableContainer>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>Hành vi</TableCell>
                    <TableCell align="right">Tổng số lần</TableCell>
                    <TableCell align="right">Trung bình/người</TableCell>
                    <TableCell align="right">Tỷ lệ thực hiện</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {[
                    { name: 'View sách', total: 1250, avg: 2.2, rate: '100%' },
                    { name: 'Purchase sách', total: 312, avg: 0.5, rate: '54.2%' },
                    { name: 'Login thành công', total: 890, avg: 1.5, rate: '100%' },
                    { name: 'Logout', total: 780, avg: 1.4, rate: '87.6%' },
                    { name: 'Truy cập trang chủ', total: 2100, avg: 3.6, rate: '100%' },
                    { name: 'Tìm kiếm sách', total: 680, avg: 1.2, rate: '68.4%' }
                  ].map((behavior) => (
                    <TableRow key={behavior.name}>
                      <TableCell>{behavior.name}</TableCell>
                      <TableCell align="right">{behavior.total.toLocaleString()}</TableCell>
                      <TableCell align="right">{behavior.avg.toFixed(1)}</TableCell>
                      <TableCell align="right">{behavior.rate}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </Paper>
        </Grid>

        {/* 7. Thống kê dữ liệu thu thập từ website */}
        <Grid item xs={12}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Thống kê dữ liệu thu thập từ website
            </Typography>
            <TableContainer>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>Chỉ số</TableCell>
                    <TableCell align="right">Giá trị</TableCell>
                    <TableCell align="right">Mô tả</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {[
                    { name: 'Tổng số người dùng đăng ký', value: '576', desc: 'Sinh viên, người đi làm' },
                    { name: 'Thời gian thu thập', value: '14 ngày', desc: '2 tuần liên tục' },
                    { name: 'Số sách trong danh mục', value: '12 cuốn', desc: 'KD và SP' },
                    { name: 'Tỷ lệ chuyển đổi', value: '54.2%', desc: 'View → Purchase' },
                    { name: 'Số session trung bình/người', value: '3.6', desc: 'Lần truy cập' },
                    { name: 'Thời gian trung bình/session', value: '8.5 phút', desc: 'Tương tác với website' }
                  ].map((stat) => (
                    <TableRow key={stat.name}>
                      <TableCell>{stat.name}</TableCell>
                      <TableCell align="right">{stat.value}</TableCell>
                      <TableCell align="right">{stat.desc}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default AnalyticsDashboard; 