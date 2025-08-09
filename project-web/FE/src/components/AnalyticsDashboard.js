import React, { useState, useEffect } from 'react';
import { Paper, Grid, Typography, Box } from '@mui/material';
import {
  Chart as ChartJS,
  CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend,
  ArcElement, PointElement, LineElement
} from 'chart.js';
import { Pie, Bar, Line } from 'react-chartjs-2';
import { getAnalytics } from '../services/customerService';

ChartJS.register(
  CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend,
  ArcElement, PointElement, LineElement
);

const normalizeAnalytics = (apiResp) => {
  // apiResp có thể là {status, data} hoặc đã là data
  const data = apiResp?.data ?? apiResp ?? {};

  const total = Number(data.total_customers ?? 0);
  const posRatio = Number(data.response_distribution?.positive ?? 0);
  const negRatio = Number(data.response_distribution?.negative ?? 0);

  const potentialCustomers = Math.round(total * posRatio);
  const nonPotentialCustomers = Math.round(total * negRatio);

  // Map feature_importance -> name/importance
  const featureImportance = (data.feature_importance ?? []).map(it => ({
    name: it.name ?? it.Feature ?? '',
    importance: Number(it.importance ?? it.Importance ?? 0),
  }));

  // Confusion matrix & ROC có thể chưa có -> để undefined
  const confusionMatrix = data.confusion_matrix ?? null;
  const rocCurve = data.roc_curve ?? null;
  const auc = data.auc ?? null;

  // Segments nếu chưa có -> null
  const segments = data.segments ?? null;

  return {
    potentialCustomers,
    nonPotentialCustomers,
    featureImportance,
    confusionMatrix, // kỳ vọng {tp, fp, tn, fn} nếu có
    rocCurve,        // kỳ vọng {fpr:[], tpr:[]} nếu có
    auc,             // số nếu có
    segments,        // [{name, count}] nếu có
  };
};

const AnalyticsDashboard = () => {
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    (async () => {
      try {
        const raw = await getAnalytics();
        const normalized = normalizeAnalytics(raw);
        setAnalytics(normalized);
      } catch (err) {
        console.error(err);
        setError('Không thể tải dữ liệu phân tích');
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  if (loading) return <Typography>Đang tải dữ liệu phân tích...</Typography>;
  if (error) return <Typography color="error">{error}</Typography>;
  if (!analytics) return null;

  // 1) Pie: phân phối
  const customerDistributionData = {
    labels: ['Khách hàng tiềm năng', 'Khách hàng không tiềm năng'],
    datasets: [{
      data: [analytics.potentialCustomers ?? 0, analytics.nonPotentialCustomers ?? 0],
      backgroundColor: ['#4CAF50', '#F44336'],
    }],
  };

  // 2) Confusion matrix (ẩn nếu thiếu)
  const hasCM = !!(analytics.confusionMatrix
    && ['tp','fp','tn','fn'].every(k => analytics.confusionMatrix[k] !== undefined));

  const confusionMatrixData = hasCM ? {
    labels: ['True Positive', 'False Positive', 'True Negative', 'False Negative'],
    datasets: [{
      label: 'Số lượng',
      data: [
        analytics.confusionMatrix.tp,
        analytics.confusionMatrix.fp,
        analytics.confusionMatrix.tn,
        analytics.confusionMatrix.fn,
      ],
      backgroundColor: ['#4CAF50', '#FFC107', '#2196F3', '#F44336'],
    }],
  } : null;

  // 3) ROC (ẩn nếu thiếu)
  const hasROC = !!(analytics.rocCurve?.fpr && analytics.rocCurve?.tpr
    && Array.isArray(analytics.rocCurve.fpr) && Array.isArray(analytics.rocCurve.tpr)
  );

  const rocCurveData = hasROC ? {
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
  } : null;

  // 4) Feature importance
  const featureImportanceData = {
    labels: (analytics.featureImportance ?? []).map(f => f.name),
    datasets: [{
      label: 'Mức độ quan trọng',
      data: (analytics.featureImportance ?? []).map(f => f.importance),
      backgroundColor: '#4CAF50',
    }],
  };

  // 5) Segmentation (ẩn nếu thiếu)
  const hasSegments = Array.isArray(analytics.segments) && analytics.segments.length > 0;
  const customerSegmentationData = hasSegments ? {
    labels: analytics.segments.map(s => s.name),
    datasets: [{
      label: 'Số lượng khách hàng',
      data: analytics.segments.map(s => s.count),
      backgroundColor: ['#FF6384','#36A2EB','#FFCE56','#4BC0C0','#9966FF'],
    }],
  } : null;

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>Phân tích dữ liệu khách hàng</Typography>

      <Grid container spacing={3}>
        {/* 1. Phân phối phân lớp khách hàng */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>Phân phối phân lớp khách hàng</Typography>
            <Box sx={{ height: 300 }}>
              <Pie data={customerDistributionData} />
            </Box>
          </Paper>
        </Grid>

        {/* 2. Ma trận nhầm lẫn (chỉ render khi có dữ liệu) */}
        {hasCM && (
          <Grid item xs={12} md={6}>
            <Paper sx={{ p: 2 }}>
              <Typography variant="h6" gutterBottom>Ma trận nhầm lẫn</Typography>
              <Box sx={{ height: 300 }}>
                <Bar
                  data={confusionMatrixData}
                  options={{ scales: { y: { beginAtZero: true } } }}
                />
              </Box>
            </Paper>
          </Grid>
        )}

        {/* 3. ROC Curve (chỉ render khi có dữ liệu) */}
        {hasROC && (
          <Grid item xs={12}>
            <Paper sx={{ p: 2 }}>
              <Typography variant="h6" gutterBottom>
                ROC Curve{analytics.auc != null ? ` (AUC: ${Number(analytics.auc).toFixed(3)})` : ''}
              </Typography>
              <Box sx={{ height: 300 }}>
                <Line
                  data={rocCurveData}
                  options={{
                    scales: {
                      x: { title: { display: true, text: 'False Positive Rate' } },
                      y: { title: { display: true, text: 'True Positive Rate' } },
                    },
                  }}
                />
              </Box>
            </Paper>
          </Grid>
        )}

        {/* 4. Feature Importance */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>Mức độ quan trọng của các đặc trưng</Typography>
            <Box sx={{ height: 300 }}>
              <Bar
                data={featureImportanceData}
                options={{
                  indexAxis: 'y',
                  scales: { x: { beginAtZero: true } },
                }}
              />
            </Box>
          </Paper>
        </Grid>

        {/* 5. Customer Segmentation (chỉ render khi có dữ liệu) */}
        {hasSegments && (
          <Grid item xs={12} md={6}>
            <Paper sx={{ p: 2 }}>
              <Typography variant="h6" gutterBottom>Phân cụm khách hàng</Typography>
              <Box sx={{ height: 300 }}>
                <Pie data={customerSegmentationData} />
              </Box>
            </Paper>
          </Grid>
        )}
      </Grid>
    </Box>
  );
};

export default AnalyticsDashboard;
