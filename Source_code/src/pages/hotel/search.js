import { useEffect, useState } from 'react';
import { useRouter } from 'next/router'
import Head from 'next/head';
import {
  Box,
  Button,
  Card,
  Container,
  Divider,
  Grid,
  InputAdornment,
  Tab,
  Tabs,
  TextField,
  Typography,
  CircularProgress
} from '@mui/material';

import { DashboardLayout } from '../../components/dashboard/dashboard-layout';
import { Search as SearchIcon } from '../../icons/search';
import { LogoHuge } from 'src/components/logo_huge';
import Router from 'next/router';




import { gtm } from '../../lib/gtm';


const Search = () => {
  
  const [noExists, setNoExists] = useState(false)
  const [loading, setLoading] = useState(false)
  


  


  useEffect(() => {
    gtm.push({ event: 'page_view' });
  }, []);

  const sendProps = () => {
    // Check if hotel exists
    
    fetch(`/checkHotel/${search}`).then(res => res.json()).then(data => {
      console.log(data)
      if ( data.hotel_id === "No such hotel") {
        setNoExists(true)
        console.log("no exists")
      } else {
        setLoading(true)
        console.log("hotel_id is " + data.hotel_id)
      

        Router.push({
          pathname: "/hotel",
          query: {
            hotel_id: data.hotel_id,
            hotel_name: data.hotel_name,
          }
        })
      }
      
    }).catch(() => console.log("error la sia"));
    


    
  }

  

  const [search, setSearch] = useState("")

  const handleSearchChange = (event) => {
    setSearch(event.target.value);
    
  };

  return (
    <>
      <Head>
        <title>
          EBW Hotel Analysis
        </title>
      </Head>

      <Box sx={{ mb: 4, mt: "20%", pl: "10%", pr: "10%" }}>
            <Grid
              container
              justifyContent={"center"}
              alignItems="center"
              flexDirection={"column"}
              
            >
              <Grid sx={{mb: 20, }}>
              <LogoHuge/>
              </Grid>
              <Grid item
              sx={{mb: 10, }}
              >

              {
                noExists ?
                <Typography variant="h5">
                  Hotel Doesn't Exists!
                </Typography>
                :

                <Typography variant="h5">
                  Search for a Hotel
                </Typography>
              }
                
                
                
              </Grid>

              
              <Grid sx={{width: "100%", maxWidth: 1000}}>
              <TextField
              
                
              defaultValue=""
              fullWidth
              size="medium"
              onChange={handleSearchChange}
              inputProps={{ }}
              InputProps={{
                startAdornment: (
                  <InputAdornment position="start">
                    <SearchIcon fontSize="large" />
                  </InputAdornment>
                )
              }}
              placeholder="Search Hotel"
            />

              </Grid>
              

<Grid
                item
                sx={{
                  display: 'flex',
                  flexWrap: 'wrap',
                  mt: 10
                }}
              >
                
                
                <Button
                  startIcon={<SearchIcon fontSize="small" />}
                  sx={{ m: 1, width: 150 }}
                  variant="contained"
                  onClick={() => sendProps()}
                >
                  {
                    loading ?

                    <CircularProgress color="secondary"  size={25}/>
                    :
                    
                    <a
                  
                  >
                    Search
                  </a> }


                  
                  
                      
                    
                </Button>
              
              </Grid>
              
              </Grid>
          </Box>
      <Box
        component="main"
        sx={{
          flex: 1,
          py: 8,
          justifyContent: "center",
          alignItems: "center",

        }}
      >
        

        
              
                
              
          

        
      </Box>
    </>
  );
};

Search.getLayout = (page) => (
  
    <DashboardLayout>
      {page}
    </DashboardLayout>
  
);

export default Search;
