import { Box, Card, CardHeader,Tooltip, Divider, Grid, List, ListItem, Typography } from '@mui/material';
import { useTheme } from '@mui/material/styles';
import { Chart } from '../chart';
import { InformationCircleOutlined  as InformationCircleOutlinedIcon} from 'src/icons/information-circle-outlined';


export const SentimentsChart = (props) => {
  const theme = useTheme();

  const chartOptions = {
    chart: {
      background: 'transparent',
      stacked: false,
      toolbar: {
        show: false
      }
    },
    colors: props.data.series.map((item) => item.color),
    fill: {
      opacity: 1
    },
    labels: ["Sentiment Score"],
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



  const chartSeries = props.data.series.map((item) => item.data);

  const total = props.data.numberOfReviews[0]['data'] + props.data.numberOfReviews[1]['data']
  

  return (
    <Card
      sx={{ height: '100%' }}
      {...props}>
      <CardHeader title={props.headerTitle} 
          action={(
          <Tooltip title="Higher the percentage, the higher the average positivity">
            <InformationCircleOutlinedIcon sx={{ color: 'action.active' }} />
          </Tooltip>
        )}


      />
      <Divider />
      <Grid
        container
        spacing={3}
        sx={{ p: 3 }}
      >
        <Grid
          item
          
          xs={12}
        >
          <Chart
            height={300}
            options={chartOptions}
            series={chartSeries}
            type="radialBar"
          />
        </Grid>
        <Grid
          item
          
          xs={12}
        >
          <Typography
            color="textSecondary"
            variant="body2"
          >
            Total
          </Typography>
          <Typography variant="h5">
            {total}
          </Typography>
          <Divider sx={{ mt: 1 }} />
          <List disablePadding>
            {props.data.numberOfReviews.map((item, index) => (
              <ListItem
                disableGutters
                divider={index + 1 < props.data.series.length}
                key={item.label}
                sx={{ display: 'flex' }}
              >
                <Box
                  sx={{
                    border: 3,
                    borderColor: item.color,
                    borderRadius: '50%',
                    height: 16,
                    mr: 1,
                    width: 16
                  }}
                />
                <Typography
                  color="textSecondary"
                  variant="body2"
                >
                  {item.label}
                </Typography>
                <Box sx={{ flexGrow: 1 }} />
                <Typography variant="subtitle2">
                  {item.data}
                </Typography>
              </ListItem>
            ))}
          </List>
        </Grid>
      </Grid>
    </Card>
  );
};
