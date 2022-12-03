import { useEffect, useState } from 'react';
import Head from 'next/head';
import {
  Box,
  Button,
  Card,
  CardActions,
  CardContent,
  Container,
  Divider,
  Grid,
  MenuItem,
  TextField,
  Typography
} from '@mui/material';
import { DashboardLayout } from '../../components/dashboard/dashboard-layout';


const Overview = () => {}

Overview.getLayout = (page) => (
  
    <DashboardLayout>
      {page}
    </DashboardLayout>
  
);

export default Overview;
