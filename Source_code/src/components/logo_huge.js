import PropTypes from 'prop-types';
import { styled } from '@mui/material/styles';

export const LogoHuge = styled((props) => {
  const { variant, ...other } = props;

  const color = variant === 'light' ? '#C1C4D6' : '#5048E5';

  return (
    
    <div style={{alignSelf: "center"}}>
      <img src={`/static/EBW.png`} alt="EBW logo" width="500"
      height="200"/>
    </div>
      
    
  );
})``;

LogoHuge.defaultProps = {
  variant: 'primary'
};

LogoHuge.propTypes = {
  variant: PropTypes.oneOf(['light', 'primary'])
};
