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
  CircularProgress,
  Alert,
  Chip,
  Card,
  CardContent,
  CardActions,
  Button,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
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
import { Bar, Pie, Line } from 'react-chartjs-2';
import { getPotentialCustomers } from '../services/customerService';

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

const PotentialCustomersChart = () => {
  const [potentialCustomers, setPotentialCustomers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [sortBy, setSortBy] = useState('probability');
  const [filterBy, setFilterBy] = useState('all');

  useEffect(() => {
    const fetchPotentialCustomers = async () => {
      try {
        setLoading(true);
        const data = await getPotentialCustomers();
        setPotentialCustomers(data);
        setError(null);
      } catch (err) {
        setError('Không thể tải danh sách khách hàng tiềm năng');
        console.error('Error fetching potential customers:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchPotentialCustomers();
  }, []);

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
        <Typography sx={{ ml: 2 }}>Đang tải dữ liệu khách hàng tiềm năng...</Typography>
      </Box>
    );
  }

  if (error) {
    return (
      <Alert severity="error" sx={{ m: 2 }}>
        {error}
      </Alert>
    );
  }

  // Lọc và sắp xếp dữ liệu
  const filteredCustomers = potentialCustomers
    .filter(customer => {
      if (filterBy === 'high') return customer.probability >= 0.7;
      if (filterBy === 'medium') return customer.probability >= 0.4 && customer.probability < 0.7;
      if (filterBy === 'low') return customer.probability < 0.4;
      return true;
    })
    .sort((a, b) => {
      if (sortBy === 'probability') return b.probability - a.probability;
      if (sortBy === 'totalSpent') return (b.totalSpent || 0) - (a.totalSpent || 0);
      if (sortBy === 'avgPurchaseValue') return (b.avgPurchaseValue || 0) - (a.avgPurchaseValue || 0);
      return 0;
    });

  // Thống kê tổng quan
  const totalCustomers = potentialCustomers.length;
  const highPotential = potentialCustomers.filter(c => c.probability >= 0.7).length;
  const mediumPotential = potentialCustomers.filter(c => c.probability >= 0.4 && c.probability < 0.7).length;
  const lowPotential = potentialCustomers.filter(c => c.probability < 0.4).length;
  const avgProbability = potentialCustomers.reduce((sum, c) => sum + c.probability, 0) / totalCustomers;

  // Dữ liệu cho biểu đồ phân phối xác suất
  const probabilityDistributionData = {
    labels: ['Thấp (&lt; 40%)', 'Trung bình (40-70%)', 'Cao (≥ 70%)'],
    datasets: [
      {
        data: [lowPotential, mediumPotential, highPotential],
        backgroundColor: ['#FF6B6B', '#FFE66D', '#4ECDC4'],
        borderWidth: 2,
        borderColor: '#fff',
      },
    ],
  };

  // Dữ liệu cho biểu đồ top 10 khách hàng tiềm năng
  const topCustomersData = {
    labels: filteredCustomers.slice(0, 10).map(c => `ID: ${c.ID}`),
    datasets: [
      {
        label: 'Xác suất mua sách (%)',
        data: filteredCustomers.slice(0, 10).map(c => c.probability * 100),
        backgroundColor: '#4CAF50',
        borderColor: '#2E7D32',
        borderWidth: 1,
      },
    ],
  };

  // Dữ liệu cho biểu đồ chi tiêu theo xác suất
  const spendingData = {
    labels: filteredCustomers.slice(0, 15).map(c => `ID: ${c.ID}`),
    datasets: [
      {
        label: 'Tổng chi tiêu (VND)',
        data: filteredCustomers.slice(0, 15).map(c => c.totalSpent || 0),
        backgroundColor: '#2196F3',
        borderColor: '#1976D2',
        borderWidth: 1,
      },
      {
        label: 'Xác suất (%)',
        data: filteredCustomers.slice(0, 15).map(c => c.probability * 100),
        backgroundColor: '#FF9800',
        borderColor: '#F57C00',
        borderWidth: 1,
        yAxisID: 'y1',
      },
    ],
  };

  const getProbabilityColor = (probability) => {
    if (probability >= 0.7) return 'success';
    if (probability >= 0.4) return 'warning';
    return 'error';
  };

  const getProbabilityLabel = (probability) => {
    if (probability >= 0.7) return 'Cao';
    if (probability >= 0.4) return 'Trung bình';
    return 'Thấp';
  };

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        Biểu đồ Danh sách Khách hàng Tiềm năng
      </Typography>

      {/* Thống kê tổng quan */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Tổng số khách hàng
              </Typography>
              <Typography variant="h4">
                {totalCustomers}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Xác suất trung bình
              </Typography>
              <Typography variant="h4">
                {(avgProbability * 100).toFixed(1)}%
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Tiềm năng cao
              </Typography>
              <Typography variant="h4" color="success.main">
                {highPotential}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Tỷ lệ tiềm năng cao
              </Typography>
              <Typography variant="h4" color="success.main">
                {((highPotential / totalCustomers) * 100).toFixed(1)}%
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Bộ lọc và sắp xếp */}
      <Paper sx={{ p: 2, mb: 3 }}>
        <Grid container spacing={2} alignItems="center">
          <Grid item xs={12} sm={6} md={3}>
            <FormControl fullWidth>
              <InputLabel>Sắp xếp theo</InputLabel>
              <Select
                value={sortBy}
                label="Sắp xếp theo"
                onChange={(e) => setSortBy(e.target.value)}
              >
                <MenuItem value="probability">Xác suất</MenuItem>
                <MenuItem value="totalSpent">Tổng chi tiêu</MenuItem>
                <MenuItem value="avgPurchaseValue">Giá trị trung bình</MenuItem>
              </Select>
            </FormControl>
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <FormControl fullWidth>
              <InputLabel>Lọc theo tiềm năng</InputLabel>
              <Select
                value={filterBy}
                label="Lọc theo tiềm năng"
                onChange={(e) => setFilterBy(e.target.value)}
              >
                <MenuItem value="all">Tất cả</MenuItem>
                <MenuItem value="high">Cao (≥ 70%)</MenuItem>
                <MenuItem value="medium">Trung bình (40-70%)</MenuItem>
                <MenuItem value="low">Thấp (&lt; 40%)</MenuItem>
              </Select>
            </FormControl>
          </Grid>
        </Grid>
      </Paper>

      {/* Biểu đồ */}
      <Grid container spacing={3}>
        {/* Biểu đồ phân phối xác suất */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Phân phối Xác suất Mua sách
            </Typography>
            <Box sx={{ height: 300 }}>
              <Pie 
                data={probabilityDistributionData}
                options={{
                  responsive: true,
                  maintainAspectRatio: false,
                  plugins: {
                    legend: {
                      position: 'bottom',
                    },
                    tooltip: {
                      callbacks: {
                        label: function(context) {
                          const total = context.dataset.data.reduce((a, b) => a + b, 0);
                          const percentage = ((context.parsed / total) * 100).toFixed(1);
                          return `${context.label}: ${context.parsed} khách hàng (${percentage}%)`;
                        }
                      }
                    }
                  }
                }}
              />
            </Box>
          </Paper>
        </Grid>

        {/* Biểu đồ top 10 khách hàng tiềm năng */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Top 10 Khách hàng Tiềm năng Cao nhất
            </Typography>
            <Box sx={{ height: 300 }}>
              <Bar 
                data={topCustomersData}
                options={{
                  responsive: true,
                  maintainAspectRatio: false,
                  scales: {
                    y: {
                      beginAtZero: true,
                      max: 100,
                      title: {
                        display: true,
                        text: 'Xác suất (%)'
                      }
                    }
                  },
                  plugins: {
                    legend: {
                      display: false
                    }
                  }
                }}
              />
            </Box>
          </Paper>
        </Grid>

        {/* Biểu đồ chi tiêu vs xác suất */}
        <Grid item xs={12}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Mối quan hệ giữa Chi tiêu và Xác suất Mua sách
            </Typography>
            <Box sx={{ height: 400 }}>
              <Bar 
                data={spendingData}
                options={{
                  responsive: true,
                  maintainAspectRatio: false,
                  scales: {
                    y: {
                      type: 'linear',
                      display: true,
                      position: 'left',
                      title: {
                        display: true,
                        text: 'Tổng chi tiêu (VND)'
                      }
                    },
                    y1: {
                      type: 'linear',
                      display: true,
                      position: 'right',
                      title: {
                        display: true,
                        text: 'Xác suất (%)'
                      },
                      grid: {
                        drawOnChartArea: false,
                      },
                    }
                  }
                }}
              />
            </Box>
          </Paper>
        </Grid>

        {/* Bảng danh sách chi tiết */}
        <Grid item xs={12}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Danh sách Chi tiết Khách hàng Tiềm năng ({filteredCustomers.length} khách hàng)
            </Typography>
            <TableContainer sx={{ maxHeight: 600 }}>
              <Table stickyHeader>
                <TableHead>
                  <TableRow>
                    <TableCell>ID</TableCell>
                    <TableCell align="right">Xác suất</TableCell>
                    <TableCell align="right">Tổng chi tiêu</TableCell>
                    <TableCell align="right">Giá trị TB</TableCell>
                    <TableCell align="right">Số lần mua</TableCell>
                    <TableCell align="center">Mức tiềm năng</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {filteredCustomers.map((customer) => (
                    <TableRow key={customer.ID} hover>
                      <TableCell>{customer.ID}</TableCell>
                      <TableCell align="right">
                        {(customer.probability * 100).toFixed(1)}%
                      </TableCell>
                      <TableCell align="right">
                        {(customer.totalSpent || 0).toLocaleString()} VND
                      </TableCell>
                      <TableCell align="right">
                        {(customer.avgPurchaseValue || 0).toLocaleString()} VND
                      </TableCell>
                      <TableCell align="right">
                        {customer.purchaseCount || 0}
                      </TableCell>
                      <TableCell align="center">
                        <Chip
                          label={getProbabilityLabel(customer.probability)}
                          color={getProbabilityColor(customer.probability)}
                          size="small"
                        />
                      </TableCell>
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

export default PotentialCustomersChart;
