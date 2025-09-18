import React, { useState } from 'react';
import {
  Container,
  Box,
  Tab,
  Tabs,
} from '@mui/material';
import CustomerList from '../components/CustomerList';
import AnalyticsDashboard from '../components/AnalyticsDashboard';
import PredictionForm from '../components/PredictionForm';
import BookList from '../components/BookList';

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
  const [tabValue, setTabValue] = useState(0);

  const handleTabChange = (event, newValue) => {
    setTabValue(newValue);
  };

  return (
    <Container maxWidth="lg">
      <Box sx={{ width: '100%', mt: 4 }}>
        <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
          <Tabs 
            value={tabValue} 
            onChange={handleTabChange} 
            aria-label="basic tabs example"
            centered
          >
            <Tab label="Dự đoán khách hàng tiềm năng" />
            <Tab label="Danh mục sách" />
            <Tab label="Danh sách khách hàng" />
            <Tab label="Phân tích dữ liệu" />
          </Tabs>
        </Box>

        <TabPanel value={tabValue} index={0}>
          <PredictionForm />
        </TabPanel>

        <TabPanel value={tabValue} index={1}>
          <BookList />
        </TabPanel>

        <TabPanel value={tabValue} index={2}>
          <CustomerList />
        </TabPanel>

        <TabPanel value={tabValue} index={3}>
          <AnalyticsDashboard />
        </TabPanel>
      </Box>
    </Container>
  );
};

export default HomePage; 