
import { useState, useEffect } from 'react';
import {
  Avatar,
  Box,
  Button,
  Card,
  CardActions,
  CardHeader,
  Divider,
  List,
  ListItem,
  ListItemAvatar,
  ListItemText,
  Typography,
  Popover,
  Modal,
} from '@mui/material';



export const ReviewsList = (props) => {

  const [modal, setModal] = useState(false)
  const [itemId, setItemId] = useState(0)

  const style = {
    position: 'absolute',
    top: '50%',
    left: '50%',
    transform: 'translate(-50%, -50%)',
    width: 400,
    bgcolor: 'background.paper',
    
    boxShadow: 24,
    pt: 2,
    px: 4,
    pb: 3,
    borderRadius: 3,
  };

  const handleClick = (index) => {
      setItemId(index);
      setModal(true)
  }



  return(
    

  <Card {...props}>
    <CardHeader title={props.headerTitle} />
    <Divider />
    <List disablePadding>
      {props.reviews.map((message, index) => (
       <a onClick={()=> handleClick(index)}>

  
        <ListItem
          divider={index + 1 < props.reviews.length}
          key={message.id}
        >
          
          <ListItemText
            disableTypography
            primary={(
              <Box
                sx={{
                  alignItems: 'center',
                  display: 'flex'
                }}
              >
                <Typography variant="h5">
                  {message.word}
                </Typography>
                
              </Box>
            )}
            secondary={(
              <Typography
                color="textSecondary"
                variant="body2"
              >
                {message.sampleReview}
              </Typography>
            )}
            sx={{ pr: 2 }}
          />
          <Typography
            color="textSecondary"
            sx={{ whiteSpace: 'nowrap' }}
            variant="subtitle1"
          >
            {message.count}
          </Typography>
        </ListItem>
        </a> 
      ))}
    </List>
    <Divider />

    <Modal
  open={modal}
  onClose={() => setModal(false)}
  aria-labelledby="modal-modal-title"
  aria-describedby="modal-modal-description"
>
  <Box sx={style}>
  <List disablePadding>
      {Object.values(props.reviews[itemId].fiveReviews).map((message, index) => (
       <a onClick={()=> setModal(true)}>

  
        <ListItem
          divider={index + 1 < props.reviews[itemId].fiveReviews.length}
          key={message.id}
        >
          
          <ListItemText
            disableTypography
            primary={(
              <Box
                sx={{
                  alignItems: 'center',
                  display: 'flex'
                }}
              >

                
              </Box>
            )}
            secondary={(
              <Typography
                color="textSecondary"
                variant="body2"
              >
                {message}
              </Typography>
            )}
            sx={{ pr: 2 }}
          />
          
        </ListItem>
        </a> 
      ))}
    </List>
  </Box>
</Modal>
    
  </Card>
  );
};
