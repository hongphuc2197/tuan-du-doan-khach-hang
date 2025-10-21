import React, { useState, useEffect } from 'react';
import {
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TablePagination,
  Typography,
  Box,
  Chip,
  IconButton,
  Collapse,
} from '@mui/material';
import KeyboardArrowDownIcon from '@mui/icons-material/KeyboardArrowDown';
import KeyboardArrowUpIcon from '@mui/icons-material/KeyboardArrowUp';
// import { getCustomers } from '../services/customerService';
import { mockCustomers } from '../data/mockData';

const formatCurrency = (value) => {
  if (value === undefined || value === null) return '0 VNĐ';
  return `${value.toLocaleString('vi-VN')} VNĐ`;
};

const columns = [
  { id: 'id', label: 'ID', minWidth: 50 },
  { id: 'age', label: 'Tuổi', minWidth: 50 },
  { id: 'income', label: 'Thu nhập', minWidth: 100, format: formatCurrency },
  { id: 'recency', label: 'Số ngày từ lần mua cuối', minWidth: 80 },
  { id: 'totalSpent', label: 'Tổng chi tiêu', minWidth: 100, format: formatCurrency },
  { id: 'avgPurchase', label: 'TB mỗi lần mua', minWidth: 100, format: formatCurrency },
  { id: 'probability', label: 'Xác suất', minWidth: 80, format: (value) => `${(value * 100).toFixed(2)}%` },
  { id: 'actions', label: 'Chi tiết', minWidth: 50 },
];

const Row = ({ customer }) => {
  const [open, setOpen] = useState(false);

  const spendingCategories = [
    { label: 'Công nghệ giáo dục', value: customer.MntWines },
    { label: 'Phương pháp giảng dạy', value: customer.MntFruits },
    { label: 'Công nghệ thông tin', value: customer.MntMeatProducts },
    { label: 'Thiết kế web', value: customer.MntFishProducts },
    { label: 'Lập trình', value: customer.MntSweetProducts },
    { label: 'Nghiên cứu khoa học', value: customer.MntGoldProds },
  ];

  const purchaseInfo = [
    { label: 'Mua sách online', value: customer.NumWebPurchases },
    { label: 'Mua sách qua catalog', value: customer.NumCatalogPurchases },
    { label: 'Mua sách tại cửa hàng', value: customer.NumStorePurchases },
    { label: 'Mua sách giảm giá', value: customer.NumDealsPurchases },
    { label: 'Truy cập website/tháng', value: customer.NumWebVisitsMonth },
  ];

  return (
    <>
      <TableRow hover>
        <TableCell>{customer.ID}</TableCell>
        <TableCell>{customer.Age}</TableCell>
        <TableCell>{formatCurrency(customer.Income)}</TableCell>
        <TableCell>{customer.Recency}</TableCell>
        <TableCell>{formatCurrency(customer.TotalSpent)}</TableCell>
        <TableCell>{formatCurrency(customer.AvgPurchaseValue)}</TableCell>
        <TableCell>{(customer.PredictionProbability * 100).toFixed(2)}%</TableCell>
        <TableCell>
          <IconButton size="small" onClick={() => setOpen(!open)}>
            {open ? <KeyboardArrowUpIcon /> : <KeyboardArrowDownIcon />}
          </IconButton>
        </TableCell>
      </TableRow>
      <TableRow>
        <TableCell style={{ paddingBottom: 0, paddingTop: 0 }} colSpan={8}>
          <Collapse in={open} timeout="auto" unmountOnExit>
            <Box sx={{ margin: 1 }}>
              <Typography variant="h6" gutterBottom component="div">
                Chi tiết khách hàng
              </Typography>
              
              <Typography variant="subtitle1" gutterBottom>
                Thông tin chi tiêu:
              </Typography>
              <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 2, mb: 2 }}>
                {spendingCategories.map((category) => (
                  <Chip
                    key={category.label}
                    label={`${category.label}: ${formatCurrency(category.value)}`}
                    variant="outlined"
                    color="primary"
                  />
                ))}
              </Box>

              <Typography variant="subtitle1" gutterBottom>
                Thông tin mua hàng:
              </Typography>
              <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 2, mb: 2 }}>
                {purchaseInfo.map((info) => (
                  <Chip
                    key={info.label}
                    label={`${info.label}: ${info.value}`}
                    variant="outlined"
                    color="secondary"
                  />
                ))}
              </Box>

              <Typography variant="subtitle1" gutterBottom>
                Thông tin gia đình:
              </Typography>
              <Box sx={{ display: 'flex', gap: 2 }}>
                <Chip
                  label={`Trẻ em: ${customer.Kidhome}`}
                  variant="outlined"
                  color="info"
                />
                <Chip
                  label={`Thanh thiếu niên: ${customer.Teenhome}`}
                  variant="outlined"
                  color="info"
                />
              </Box>
            </Box>
          </Collapse>
        </TableCell>
      </TableRow>
    </>
  );
};

const CustomerList = () => {
  const [customers, setCustomers] = useState([]);
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchCustomers = async () => {
      try {
        // Sử dụng dữ liệu mẫu thay vì gọi API
        setCustomers(mockCustomers);
        setLoading(false);
      } catch (err) {
        setError('Không thể tải dữ liệu khách hàng');
        setLoading(false);
      }
    };

    fetchCustomers();
  }, []);

  const handleChangePage = (event, newPage) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event) => {
    setRowsPerPage(+event.target.value);
    setPage(0);
  };

  if (loading) return <Typography>Đang tải...</Typography>;
  if (error) return <Typography color="error">{error}</Typography>;

  return (
    <Paper sx={{ width: '100%', overflow: 'hidden' }}>
      <Box p={3}>
        <Typography variant="h5" gutterBottom>
          Danh sách sinh viên tiềm năng mua sách công nghệ giáo dục ({customers.length} sinh viên)
        </Typography>
      </Box>
      <TableContainer sx={{ maxHeight: 600 }}>
        <Table stickyHeader aria-label="sticky table">
          <TableHead>
            <TableRow>
              {columns.map((column) => (
                <TableCell
                  key={column.id}
                  align="left"
                  style={{ minWidth: column.minWidth, fontWeight: 'bold' }}
                >
                  {column.label}
                </TableCell>
              ))}
            </TableRow>
          </TableHead>
          <TableBody>
            {customers
              .slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
              .map((customer) => (
                <Row key={customer.ID} customer={customer} />
              ))}
          </TableBody>
        </Table>
      </TableContainer>
      <TablePagination
        rowsPerPageOptions={[10, 25, 50]}
        component="div"
        count={customers.length}
        rowsPerPage={rowsPerPage}
        page={page}
        onPageChange={handleChangePage}
        onRowsPerPageChange={handleChangeRowsPerPage}
        labelRowsPerPage="Số hàng mỗi trang"
      />
    </Paper>
  );
};

export default CustomerList; 