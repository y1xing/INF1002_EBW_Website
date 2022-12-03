import numeral from 'numeral';
import { Box, Card, CardContent, CardHeader, Divider } from '@mui/material';
import { useTheme } from '@mui/material/styles';
import { Chart } from '../chart';

export const PriceRatingsChart = (props) => {
  const theme = useTheme();

  const chartOptions = {
    chart: {
      background: 'transparent',
      stacked: false,
      toolbar: {
        show: false
      }
    },
    colors: [
      '#2F3EB1',
      '#4655CE',
      '#6E7AD8',
      '#9DA4DD',
      '#B9BDDF',
      '#E6E8F0',
    ],
    dataLabels: {
      enabled: false
    },
    fill: {
      opacity: 1
    },
    grid: {
      borderColor: theme.palette.divider
    },
    plotOptions: {
      bar: {
        barHeight: '65',
        distributed: true,
        horizontal: true
      }
    },
    theme: {
      mode: theme.palette.mode
    },
    tooltip: {
      y: {
        
          formatter: (value) => numeral(value).format('0,0.00')
      }
    },
    xaxis: {
      axisBorder: {
        color: theme.palette.divider,
        show: true
      },
      axisTicks: {
        color: theme.palette.divider,
        show: true
      },
      categories: props.data.categories
    }
  };

  const chartSeries = [
    {
      name: 'Sales',
      data: props.data.values
    }
  ];

  return (
    <Card {...props}>
      <CardHeader title={props.headerTitle} />
      <Divider />
      <CardContent>
        <Box
          sx={{
            display: 'flex',
            justifyContent: 'center'
          }}
        >
          
        </Box>
        <Chart
          height={350}
          options={chartOptions}
          series={chartSeries}
          type="bar"
        />
      </CardContent>
    </Card>
  );
};
