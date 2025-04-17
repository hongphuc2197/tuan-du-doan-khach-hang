import React from 'react';
import {
  AppBar,
  Toolbar,
  Typography,
  Container,
  Box,
} from '@mui/material';
import PeopleAltIcon from '@mui/icons-material/PeopleAlt';

const Navbar = () => {
  return (
    <AppBar position="static">
      <Container maxWidth="xl">
        <Toolbar disableGutters>
          <PeopleAltIcon sx={{ display: { xs: 'none', md: 'flex' }, mr: 1 }} />
          <Typography
            variant="h6"
            noWrap
            component="div"
            sx={{
              mr: 2,
              display: { xs: 'none', md: 'flex' },
              fontWeight: 700,
              color: 'inherit',
              textDecoration: 'none',
            }}
          >
            Hệ thống Dự đoán Khách hàng Tiềm năng
          </Typography>

          <Box sx={{ flexGrow: 1 }} />

          <Box sx={{ display: { xs: 'none', md: 'flex' } }}>
            <Typography
              variant="body1"
              sx={{
                color: 'inherit',
                textDecoration: 'none',
                marginLeft: 2,
              }}
            >
              Kyanon Digital
            </Typography>
          </Box>
        </Toolbar>
      </Container>
    </AppBar>
  );
};

export default Navbar; 