import { Avatar, Box, Button, Card, CardActions, Divider, Grid, Typography } from '@mui/material';
import { alpha, useTheme } from '@mui/material/styles';
import { Chart } from '../chart';



const PieChart = (props) => {
  const theme = useTheme();

  const chartOptions = {
    chart: {
      background: 'transparent',
      stacked: false,
      toolbar: {
        show: false
      }
    },
    colors: [props.color],
    fill: {
      opacity: 1
    },
    labels: [props.name],
    plotOptions: {
      radialBar: {
        dataLabels: {
          name: {
            show: true,
            color: theme.palette.text.secondary,
            fontSize: '12px',
            fontWeight: 400,
            offsetY: 20
          },
          value: {
            color: theme.palette.text.primary,
            fontSize: '18px',
            fontWeight: 600,
            offsetY: -20
          },

        },
        hollow: {
          size: '60%'
        },
        track: {
          background: "#F3F4F7"
        }
      }
    },
    theme: {
      mode: theme.palette.mode
    }
  };

  const chartSeries = [props.value];

  return (
    <Chart
          height={250}
          options={chartOptions}
          series={chartSeries}
          type="radialBar"
          width={200}
      />
  );
};


export const GeneralCategoriesCharts = (props) => (
  <Grid
    container
    spacing={3}
  >
    <Grid
      item
      md={2}
      sm={4}
      xs={6}
    >
      
        <Box
          sx={{
            alignItems: 'center',
            display: 'flex',
            justifyContent: 'center',
            
          }}
        >
          
            
            <PieChart name="Staff" value={props.cat_staff * 10} color="#552586"/>
            
          
          
        </Box>
        
      
    </Grid>
    <Grid
      item
      md={2}
      sm={4}
      xs={6}
    >
      
        <Box
          sx={{
            alignItems: 'center',
            display: 'flex',
            justifyContent: 'center',
            
          }}
        >
          
            
            <PieChart name="Facilities" value={props.cat_facilities  * 10} color="#6A359C"/>
            
          
          
        </Box>
        
      
    </Grid>
    <Grid
      item
      md={2}
      sm={4}
      xs={6}
    >
      
        <Box
          sx={{
            alignItems: 'center',
            display: 'flex',
            justifyContent: 'center',
            
          }}
        >
          
            
            <PieChart name="Cleanliness" value={props.cat_cleaniness  * 10} color="#804FB3"/>
            
          
          
        </Box>
        
      
    </Grid>
    <Grid
      item
      md={2}
      sm={4}
      xs={6}
    >
      
        <Box
          sx={{
            alignItems: 'center',
            display: 'flex',
            justifyContent: 'center',
            
          }}
        >
          
            
            <PieChart name="Comfort" value={props.cat_comfort  * 10} color="#9969C7"/>
            
          
          
        </Box>
        
      
    </Grid>
    <Grid
      item
      md={2}
      sm={4}
      xs={6}
    >
      
        <Box
          sx={{
            alignItems: 'center',
            display: 'flex',
            justifyContent: 'center',
            
          }}
        >
          
            
            <PieChart name="Value" value={props.cat_value_for_money  * 10} color="#B589D6"/>
            
          
          
        </Box>
        
      
    </Grid>
    <Grid
      item
      md={2}
      sm={4}
      xs={6}
    >
      
        <Box
          sx={{
            alignItems: 'center',
            display: 'flex',
            justifyContent: 'center',
            
          }}
        >
          
            
            <PieChart name="Location" value={props.cat_location  * 10} color="#D7B0F4"/>
            
          
          
        </Box>
        
      
    </Grid>
    
    
  </Grid>
  
);
