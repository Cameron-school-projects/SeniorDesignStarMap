
import { shape } from 'prop-types';
import React from 'react';
import Button from './button';

// Define the props in case you need to customize labels or add more props in the future
interface LeftColumnProps {
  labels: string[];
}


const LeftColumn: React.FC<LeftColumnProps> = ({ labels }) => {
  return (
    <div style={{ width: '25%', float: 'left', padding: '10px', textAlign: 'center', fontFamily: 'monospace', fontSize: '25px' }}> {/* Adjust the styling as needed */}
      {labels.map((label, index) => (
        <div key={index} style={{ marginBottom: '20px' }}> {/* This div wraps each label-input pair */}
          <label style = {{display: 'block', marginBottom: '10px' }}>
            {label}: </label>
            <input type="text" style={{height: '5vh', width: '700%', border: '2px solid #007bff' , borderRadius: '8px', padding: '2px', fontFamily: 'monospace', fontSize: '15px' }}  />
          
        </div>
      ))}
        <Button buttonStyle={{ color: 'gray', rounded: 'lg', size: 'md' }}>
        Map it!
     </Button>
    </div>
  );
};

export default LeftColumn;

/* <button style={{padding: '8px 16px', marginTop: '10px', color: 'white', borderRadius: '10px', height: '20px', }}>
        Enter
      </button> */