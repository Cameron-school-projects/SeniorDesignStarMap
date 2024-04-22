
import { shape } from 'prop-types';
import React from 'react';
import Button from './button';
import axios, {isCancel, AxiosError} from 'axios';

// Define the props in case you need to customize labels or add more props in the future
interface LeftColumnProps {
  labels: string[];
  labelImageSet:Function;
  unlabeledSet:Function;
  imageToDownload:string;
}


const LeftColumn: React.FC<LeftColumnProps> = ({ labels,labelImageSet,unlabeledSet,imageToDownload }) => {
  function testPost(){
    console.log("test")
    axios.post('http://localhost:5000/getStarData', {

    lat: '33-52-11.44S',
    lon: '151-12-29.82E',
    date: '05/08/2002',
    time: '1:30PM',
    
  })

  .then((response: any)=>{

    console.log(response);
    let imageToDisplay = "data:image/png;base64,"+response.data[0]
    unlabeledSet(imageToDisplay)
    imageToDisplay = "data:image/png;base64,"+response.data[1]
    labelImageSet(imageToDisplay)

  })
}
function downloadImage(){
  var a = document.createElement("a"); //Create <a>
  a.href = imageToDownload; //Image Base64 Goes here
  a.download = "StarMap.png"; //File name Here
  a.click(); //Downloaded file
}
  return (
    <div style={{ width: '25%', float: 'left', padding: '10px', textAlign: 'center', fontFamily: 'monospace', fontSize: '25px' }}> {/* Adjust the styling as needed */}
      {labels.map((label, index) => (
        <div key={index} style={{ marginBottom: '20px' }}> {/* This div wraps each label-input pair */}
          <label style = {{display: 'block', marginBottom: '10px' }}>
            {label}: </label>
            <input type="text" style={{height: '5vh', width: '700%', border: '2px solid #007bff' , borderRadius: '8px', padding: '2px', fontFamily: 'monospace', fontSize: '15px' }}  />
          
        </div>
      ))}
        <Button buttonStyle={{ color: 'gray', rounded: 'lg', size: 'md' }} onClick={testPost}>
        Map it!
     </Button>
     <Button buttonStyle={{ color: 'gray', rounded: 'lg', size: 'md' }} onClick={downloadImage}>
      Download Current Map
      </Button>
    </div>
  );
};

export default LeftColumn;

/* <button style={{padding: '8px 16px', marginTop: '10px', color: 'white', borderRadius: '10px', height: '20px', }}>
        Enter
      </button> */