import { useEffect, useState } from 'react';
import { useRouter } from 'next/router'
import Head from 'next/head';
import { Box, Popover, Button, Container, Grid, MenuItem, TextField, Typography, CircularProgress } from '@mui/material';

import { DashboardLayout } from '../../components/dashboard/dashboard-layout';
import { GeneralCategoriesCharts } from 'src/components/hotel/general_categories';
import { PriceRatingsChart } from 'src/components/hotel/prices_ratings';
import { Search as SearchIcon } from '../../icons/search';
import { DemandChart } from 'src/components/hotel/demand';
import { ReviewsList } from 'src/components/hotel/reviews_list';
import { SentimentsChart } from 'src/components/hotel/sentiments';


import { gtm } from '../../lib/gtm';


const Hotel = () => {
  const router = useRouter()
  const { hotel_id, hotel_name } = router.query


  const [loading, setLoading] = useState(true)
  const [loading2, setLoading2] = useState(false)

  const [currentTime, setCurrentTime] = useState("1000");
  const [generalData, setGeneralData] = useState({})
  const [roomAverageRatingData, setRoomAverageRatingData] = useState({});
  const [roomDemandData, setRoomDemandData] = useState({});
  const [wordFrequencyData, setWordFrequencyData] = useState({});
  const [negativeWordFrequencyData, setNegativeWordFrequencyData] = useState({});
  const [countryData, setCountryData] = useState([])
  const [travelerData, setTravelerData] = useState([])
  const [country, setCountry] = useState("everything");
  const [traveler, setTraveler] = useState("everything");
  const [sentimentData, setSentimentData] = useState({})

  const sleep = ms => new Promise(r => setTimeout(r, ms));

  const getGeneralData = async () => {
    fetch(`/general/${hotel_id}`).then(res => res.json()).then(data => {
      console.log(data)
      setGeneralData(data)
    }).catch(() => console.log("errorrr la sia"));
  }

  const getRoomAverageRatingData = async () => {
    fetch(`/room_types_average_rating/${hotel_id}`).then(res => res.json()).then(data => {
      console.log(data)
      setRoomAverageRatingData(data)
      
    }).catch(() => console.log("errorrr la sia2"));
  }

  const getRoomDemandData = async () => {
    fetch(`/room_types_no_reviews/${hotel_id}`).then(res => res.json()).then(data => {
      console.log(data)
      setRoomDemandData(data)
      
    }).catch(() => console.log("errorrr la sia3"));
  }


  const getPositiveWordFrequency = async (country, traveler) => {
    fetch(`/wordFrequency/${hotel_id}+${country}+${traveler}`).then(res => res.json()).then(data => {
      console.log(data)
      setWordFrequencyData(data)
      
    }).catch(() => console.log("errorrr la sia4"));
  }

  const getNegativeWordFrequency = async (country, traveler) => {
    fetch(`/negwordFrequency/${hotel_id}+${country}+${traveler}`).then(res => res.json()).then(data => {
      console.log(data)
      setNegativeWordFrequencyData(data)
      
    }).catch(() => console.log("errorrr la sia4"));
  }

  const getCountriesAndTraveler = async () => {
    fetch(`/countryAndTraveler/${hotel_id}`).then(res => res.json()).then(data => {
      const {countries, traveler} = data;
      setCountryData(countries)
      setTravelerData(traveler)
      
      
    }).catch(() => console.log("errorrr la sia4"));
  }

  const getSentiment = async (country, traveler) => {
    fetch(`/sentiment/${hotel_id}+${country}+${traveler}`).then(res => res.json()).then(data => {
      console.log(data)
      setSentimentData(data)
      
    }).catch(() => console.log("errorrr la sia4"));
  }


  const delay = ms => new Promise(res => setTimeout(res, ms));


  useEffect(async () => {
    setLoading(true)

    await getGeneralData()
    await getCountriesAndTraveler()
    await getRoomAverageRatingData()
    await getRoomDemandData()
    await getPositiveWordFrequency("everything", "everything")
    await getNegativeWordFrequency("everything", "everything")
    await getSentiment("everything", "everything")
    
  
    await delay(1000)
    console.log("hello")
    setLoading(false)
    
  }, [])


  useEffect(() => {
    gtm.push({ event: 'page_view' });
  }, []);

  const numberOfStars = (number) => {
    const numberOfStars = []
    for (let i=0; i< number; i++) {
      numberOfStars.push(<img src='/static/icons/star.svg' height={30} width={50} alt="star"/>)
    }
    return numberOfStars
  }

  const handleCountryChange = (event) => {
    setCountry(event.target.value);
  };

  const handleTravelerChange = (event) => {
    setTraveler(event.target.value);
  };

  const handleFilter = async () => {
      // API Call for the positive and negative reviews
      setLoading2(true)
      await delay(1000)
      await getPositiveWordFrequency(country, traveler)
      await getNegativeWordFrequency(country, traveler)
      await getSentiment(country, traveler)

      setLoading2(false)

  }

  return (


    <>
      <Head>
        <title>
        {hotel_name}'s Review
        </title>
      </Head>

      
  
          
  



      <Box
        component="main"
        sx={{
          flexGrow: 1,
          py: 8,
          
        }}
      >
        {
          loading ?
          <Box 
          sx={{ml: "45%", mt: "45%"}}
          >
              <CircularProgress size={40}/>
          </Box>
          
          :
        



        <Container maxWidth="xl">
          <Box sx={{ mb: 4, mt: 6 }}>
            <Grid
              container
              justifyContent={"center"}
              alignItems="center"
              flexDirection={"column"}
              
            >
              <Grid item
              
              >
                <Typography variant="h1">
                  {generalData.hotel_name}
                </Typography>
                
                
              </Grid>
              <Grid alignSelf={"center"}>
                {
                  numberOfStars(generalData.hotel_stars)
                }

                  {/* <img src='/static/icons/star.svg' height={30} width={50} alt="star"/>
                  <img src='/static/icons/star.svg' height={30} width={50} alt="star"/>
                  <img src='/static/icons/star.svg' height={30} width={50} alt="star"/> */}
                  </Grid>
              <Grid item>
              <Grid item
              
              >
                <Typography variant="h7">
                {generalData.address}
                </Typography>
                
                
                
              </Grid>

              </Grid>
              
              
              
      
            </Grid>
          </Box>

          <GeneralCategoriesCharts 
            cat_cleaniness={generalData.cat_cleaniness}
            cat_comfort={generalData.cat_comfort}
            cat_facilities={generalData.cat_facilities}
            cat_location={generalData.cat_location}
            cat_staff={generalData.cat_staff}
            cat_value_for_money={generalData.cat_value_for_money}
            
             />


          
          <Box sx={{ mb: 4, mt: 6 }}>
            <Grid
              container
              justifyContent={"center"}
              alignItems="center"
              flexDirection={"column"}
              
            >
              <Grid item
              
              >
                <Typography variant="h1">
                  Room Types
                </Typography>
                
                
              </Grid>
              

              
              
              
              
        
            </Grid>
          </Box>

          <Grid
            container
            spacing={4}
          >
          <Grid
              item
              md={6}
              xs={12}
            >
              <PriceRatingsChart data={generalData.roomtypes_clean} headerTitle={"Prices"}/>
              {/* <FinanceSalesByContinent data={roomTypesData} headerTitle={"Ratings"}/> */}
            </Grid>
            <Grid
              item
              md={6}
              xs={12}
            >
              <PriceRatingsChart data={roomAverageRatingData} headerTitle={"Ratings"}/>
            </Grid>
            </Grid>

          <Box sx={{ mt: 4 }}>
            <Grid
              container
              spacing={4}
            >
              <Grid
                item
                md={12}
                xs={12}
              >
                <DemandChart data={roomDemandData} sx={{ height: '100%' }} />
              </Grid>
              
              
            </Grid>
          </Box>
          <Box sx={{ mb: 4, mt: 6 }}>
            <Grid
              container
              justifyContent={"center"}
              alignItems="center"
              flexDirection={"column"}
              
            >
              <Grid item
              
              >
                <Typography variant="h1">
                  Hotel Reviews Analysis
                </Typography>
                
                
              </Grid>

              <Box
              sx={{
                alignItems: 'center',
                display: 'flex',
                flexWrap: 'wrap',
                m: -1.5,
                p: 3
              }}
            >
              <Box
                component="form"
                onSubmit={() => {}}
                sx={{
                  flexGrow: 1,
                  m: 1.5
                }}
              >

            

                <TextField
                label="Country"
                name="country"
                onChange={handleCountryChange}
                select
                SelectProps={{ native: true }}
                sx={{ m: 1.5 }}
                value={country}
              >
                {countryData.map((option) => (
                  <option
            
                    value={option}
                  >
                    {option}
                  </option>
                ))}
              </TextField>
              </Box>
              <TextField
                label="Type of Traveller"
                name="type of traveller"
                onChange={handleTravelerChange}
                select
                SelectProps={{ native: true }}
                sx={{ m: 1.5 }}
                value={traveler}
              >
                {travelerData.map((option) => (
                  <option

                    value={option}
                  >
                    {option}
                  </option>
                ))}
              </TextField>
            </Box>

            <Grid
                item
                sx={{
                  display: 'flex',
                  flexWrap: 'wrap',
                  m: -1
                }}
              >
                
                
                <Button
                  startIcon={<SearchIcon fontSize="small" />}
                  sx={{ m: 1, width: 150 }}
                  variant="contained"
                  
                  onClick={() => {handleFilter()}}
                >
                  Filter
                </Button>
              </Grid>
              

              
              
              
              
        
            </Grid>
          </Box>

          {
            loading2 ?
          <Box 
          sx={{ml: "45%", mt: "25%"}}
          >
              <CircularProgress size={40}/>
          </Box>
          
          :
          



          <Box sx={{ mb: 4, mt: 6, top: 0, flexDirection: "row" }}>
            <Grid
              container
              spacing={5}
              alignItems="center"
              flexDirection={"row"}
              
            >
              
              <Grid
              item
              md={6}
              xs={12}
            >
              <ReviewsList reviews={wordFrequencyData} headerTitle={"Positive Reviews"} />
            </Grid>
            <Grid
              item
              md={6}
              xs={12}
            >
              <ReviewsList reviews={negativeWordFrequencyData} headerTitle={"Negative Reviews"} />
            </Grid>
                

              
        
            </Grid>
          </Box>

        }

        {
          loading2 ?
          null:

        
          <Box sx={{ mb: 4, mt: 6, flexDirection: "row" }}>
            <Grid
              container
              spacing={5}
              alignItems="center"
              flexDirection={"row"}
              
            >

          <Grid
              item
              md={4}
              xs={12}
            >
              <SentimentsChart headerTitle={"Staff"} data={sentimentData.staff} total={100}/>
            </Grid>
            <Grid
              item
              md={4}
              xs={12}
            >
              <SentimentsChart headerTitle={"Facilities"} data={sentimentData.facilities} total={100}/>
            </Grid>
            <Grid
              item
              md={4}
              xs={12}
            >
              <SentimentsChart headerTitle={"Cleanliness"} data={sentimentData.cleanliness} total={100}/>
            </Grid>
            <Grid
              item
              md={4}
              xs={12}
            >
              <SentimentsChart headerTitle={"Comfort"} data={sentimentData.comfort} total={100}/>
            </Grid>
            <Grid
              item
              md={4}
              xs={12}
            >
              <SentimentsChart headerTitle={"Value"} data={sentimentData['value for money']} total={100}/>
            </Grid>
            <Grid
              item
              md={4}
              xs={12}
            >
              <SentimentsChart headerTitle={"Location"} data={sentimentData.location}/>
            </Grid>
              
              
                

              
        
            </Grid>
          </Box>
        }

        </Container>
        }
      </Box>
      
    </>
  );
};

Hotel.getLayout = (page) => (
  
    <DashboardLayout>
      {page}
    </DashboardLayout>
  
);

export default Hotel;
