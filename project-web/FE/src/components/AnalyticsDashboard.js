import React, { useState, useEffect } from 'react';
import {
  Paper,
  Grid,
  Typography,
  Box,
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
import { Pie, Bar, Line } from 'react-chartjs-2';
import { getAnalytics } from '../services/customerService';

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
        const data = await getAnalytics();
        setAnalytics(data);
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

  // 1. Biểu đồ phân phối phân lớp khách hàng (Pie chart)
  const customerDistributionData = {
    labels: ['Khách hàng tiềm năng', 'Khách hàng không tiềm năng'],
    datasets: [
      {
        data: [analytics.potentialCustomers, analytics.nonPotentialCustomers],
        backgroundColor: ['#4CAF50', '#F44336'],
      },
    ],
  };

  // 2. Confusion Matrix (Bar chart)
  const confusionMatrixData = {
    labels: ['True Positive', 'False Positive', 'True Negative', 'False Negative'],
    datasets: [
      {
        label: 'Số lượng',
        data: [
          analytics.confusionMatrix.tp,
          analytics.confusionMatrix.fp,
          analytics.confusionMatrix.tn,
          analytics.confusionMatrix.fn,
        ],
        backgroundColor: ['#4CAF50', '#FFC107', '#2196F3', '#F44336'],
      },
    ],
  };

  // 3. ROC Curve
  const rocCurveData = {
    labels: analytics.rocCurve.fpr.map((_, i) => i),
    datasets: [
      {
        label: 'ROC Curve',
        data: analytics.rocCurve.tpr,
        borderColor: '#2196F3',
        backgroundColor: 'rgba(33, 150, 243, 0.1)',
        fill: true,
      },
      {
        label: 'Random Guess',
        data: analytics.rocCurve.fpr,
        borderColor: '#9E9E9E',
        borderDash: [5, 5],
      },
    ],
  };

  // 4. Feature Importance
  const featureImportanceData = {
    labels: analytics.featureImportance.map(f => f.name),
    datasets: [
      {
        label: 'Mức độ quan trọng',
        data: analytics.featureImportance.map(f => f.importance),
        backgroundColor: '#4CAF50',
      },
    ],
  };

  // 5. Customer Segmentation
  const customerSegmentationData = {
    labels: analytics.segments.map(s => s.name),
    datasets: [
      {
        label: 'Số lượng khách hàng',
        data: analytics.segments.map(s => s.count),
        backgroundColor: [
          '#FF6384',
          '#36A2EB',
          '#FFCE56',
          '#4BC0C0',
          '#9966FF',
        ],
      },
    ],
  };

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        Phân tích dữ liệu khách hàng
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

        {/* 2. Confusion Matrix */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Ma trận nhầm lẫn
            </Typography>
            <Box sx={{ height: 300 }}>
              <Bar
                data={confusionMatrixData}
                options={{
                  scales: {
                    y: {
                      beginAtZero: true,
                    },
                  },
                }}
              />
            </Box>
          </Paper>
        </Grid>

        {/* 3. ROC Curve */}
        <Grid item xs={12}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              ROC Curve (AUC: {analytics.auc.toFixed(3)})
            </Typography>
            <Box sx={{ height: 300 }}>
              <Line
                data={rocCurveData}
                options={{
                  scales: {
                    x: {
                      title: {
                        display: true,
                        text: 'False Positive Rate',
                      },
                    },
                    y: {
                      title: {
                        display: true,
                        text: 'True Positive Rate',
                      },
                    },
                  },
                }}
              />
            </Box>
          </Paper>
        </Grid>

        {/* 4. Feature Importance */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Mức độ quan trọng của các đặc trưng
            </Typography>
            <Box sx={{ height: 300 }}>
              <Bar
                data={featureImportanceData}
                options={{
                  indexAxis: 'y',
                  scales: {
                    x: {
                      beginAtZero: true,
                    },
                  },
                }}
              />
            </Box>
          </Paper>
        </Grid>

        {/* 5. Customer Segmentation */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Phân cụm khách hàng
            </Typography>
            <Box sx={{ height: 300 }}>
              <Pie data={customerSegmentationData} />
            </Box>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default AnalyticsDashboard; 