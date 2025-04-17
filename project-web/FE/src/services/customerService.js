import axios from 'axios';

const API_URL = 'http://localhost:5000/api';

export const getCustomers = async () => {
  try {
    const response = await axios.get(`${API_URL}/customers`);
    return response.data;
  } catch (error) {
    console.error('Error fetching customers:', error);
    throw error;
  }
};

export const predictCustomer = async (customerData) => {
  try {
    const response = await axios.post(`${API_URL}/predict`, customerData);
    return response.data;
  } catch (error) {
    console.error('Error predicting customer:', error);
    throw error;
  }
};

export const getAnalytics = async () => {
  try {
    const response = await axios.get(`${API_URL}/analytics`);
    return response.data;
  } catch (error) {
    console.error('Error fetching analytics:', error);
    throw error;
  }
}; 