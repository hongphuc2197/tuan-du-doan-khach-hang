import React, { useState } from 'react';
import {
  Container,
  Paper,
  Typography,
  TextField,
  Button,
  Grid,
  Box,
  Alert,
  Tab,
  Tabs,
} from '@mui/material';
import { predictCustomer } from '../services/customerService';
import CustomerList from '../components/CustomerList';
import AnalyticsDashboard from '../components/AnalyticsDashboard';

function TabPanel(props) {
  const { children, value, index, ...other } = props;
  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`simple-tabpanel-${index}`}
      aria-labelledby={`simple-tab-${index}`}
      {...other}
    >
      {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
    </div>
  );
}

const HomePage = () => {
  const [formData, setFormData] = useState({
    income: '',
    kidhome: '',
    teenhome: '',
    recency: '',
    mntWines: '',
    mntFruits: '',
    mntMeatProducts: '',
    mntFishProducts: '',
    mntSweetProducts: '',
    mntGoldProds: '',
    numDealsPurchases: '',
    numWebPurchases: '',
    numCatalogPurchases: '',
    numStorePurchases: '',
    numWebVisitsMonth: '',
  });

  const [prediction, setPrediction] = useState(null);
  const [error, setError] = useState(null);
  const [tabValue, setTabValue] = useState(0);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const result = await predictCustomer(formData);
      setPrediction(result);
      setError(null);
    } catch (err) {
      setError('Có lỗi xảy ra khi dự đoán. Vui lòng thử lại.');
      setPrediction(null);
    }
  };

  const handleTabChange = (event, newValue) => {
    setTabValue(newValue);
  };

  return (
    <Container maxWidth="lg">
      <Box sx={{ width: '100%', mt: 4 }}>
        <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
          <Tabs value={tabValue} onChange={handleTabChange} aria-label="basic tabs example">
            <Tab label="Dự đoán khách hàng" />
            <Tab label="Danh sách khách hàng tiềm năng" />
            <Tab label="Phân tích dữ liệu" />
          </Tabs>
        </Box>

        <TabPanel value={tabValue} index={0}>
          <Paper elevation={3} sx={{ p: 4 }}>
            <Typography variant="h5" gutterBottom>
              Dự đoán khách hàng tiềm năng
            </Typography>
            <form onSubmit={handleSubmit}>
              <Grid container spacing={3}>
                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth
                    label="Thu nhập"
                    name="income"
                    type="number"
                    value={formData.income}
                    onChange={handleChange}
                    required
                  />
                </Grid>
                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth
                    label="Số trẻ em"
                    name="kidhome"
                    type="number"
                    value={formData.kidhome}
                    onChange={handleChange}
                    required
                  />
                </Grid>
                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth
                    label="Số thanh thiếu niên"
                    name="teenhome"
                    type="number"
                    value={formData.teenhome}
                    onChange={handleChange}
                    required
                  />
                </Grid>
                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth
                    label="Số ngày từ lần mua cuối"
                    name="recency"
                    type="number"
                    value={formData.recency}
                    onChange={handleChange}
                    required
                  />
                </Grid>
                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth
                    label="Chi tiêu rượu"
                    name="mntWines"
                    type="number"
                    value={formData.mntWines}
                    onChange={handleChange}
                    required
                  />
                </Grid>
                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth
                    label="Chi tiêu trái cây"
                    name="mntFruits"
                    type="number"
                    value={formData.mntFruits}
                    onChange={handleChange}
                    required
                  />
                </Grid>
                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth
                    label="Chi tiêu thịt"
                    name="mntMeatProducts"
                    type="number"
                    value={formData.mntMeatProducts}
                    onChange={handleChange}
                    required
                  />
                </Grid>
                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth
                    label="Chi tiêu cá"
                    name="mntFishProducts"
                    type="number"
                    value={formData.mntFishProducts}
                    onChange={handleChange}
                    required
                  />
                </Grid>
                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth
                    label="Chi tiêu đồ ngọt"
                    name="mntSweetProducts"
                    type="number"
                    value={formData.mntSweetProducts}
                    onChange={handleChange}
                    required
                  />
                </Grid>
                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth
                    label="Chi tiêu vàng"
                    name="mntGoldProds"
                    type="number"
                    value={formData.mntGoldProds}
                    onChange={handleChange}
                    required
                  />
                </Grid>
                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth
                    label="Số lần mua khuyến mãi"
                    name="numDealsPurchases"
                    type="number"
                    value={formData.numDealsPurchases}
                    onChange={handleChange}
                    required
                  />
                </Grid>
                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth
                    label="Số lần mua qua web"
                    name="numWebPurchases"
                    type="number"
                    value={formData.numWebPurchases}
                    onChange={handleChange}
                    required
                  />
                </Grid>
                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth
                    label="Số lần mua qua catalog"
                    name="numCatalogPurchases"
                    type="number"
                    value={formData.numCatalogPurchases}
                    onChange={handleChange}
                    required
                  />
                </Grid>
                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth
                    label="Số lần mua tại cửa hàng"
                    name="numStorePurchases"
                    type="number"
                    value={formData.numStorePurchases}
                    onChange={handleChange}
                    required
                  />
                </Grid>
                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth
                    label="Số lần truy cập web trong tháng"
                    name="numWebVisitsMonth"
                    type="number"
                    value={formData.numWebVisitsMonth}
                    onChange={handleChange}
                    required
                  />
                </Grid>
                <Grid item xs={12}>
                  <Button
                    type="submit"
                    variant="contained"
                    color="primary"
                    size="large"
                  >
                    Dự đoán
                  </Button>
                </Grid>
              </Grid>
            </form>

            {error && (
              <Alert severity="error" sx={{ mt: 2 }}>
                {error}
              </Alert>
            )}

            {prediction && (
              <Box mt={3}>
                <Alert severity={prediction.isPotential ? "success" : "info"}>
                  {prediction.isPotential
                    ? `Khách hàng này là khách hàng tiềm năng với xác suất ${(prediction.probability * 100).toFixed(2)}%`
                    : "Khách hàng này không phải là khách hàng tiềm năng"}
                </Alert>
              </Box>
            )}
          </Paper>
        </TabPanel>

        <TabPanel value={tabValue} index={1}>
          <CustomerList />
        </TabPanel>

        <TabPanel value={tabValue} index={2}>
          <AnalyticsDashboard />
        </TabPanel>
      </Box>
    </Container>
  );
};

export default HomePage; 