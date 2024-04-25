'use client'
import { shape } from 'prop-types';
import React from 'react';
import Button from './button';
import axios, {isCancel, AxiosError} from 'axios';
import TimePicker from 'react-time-picker';
import { TextField } from '@mui/material';
import dayjs, { Dayjs } from 'dayjs';
import { useState } from 'react';
import { DemoContainer } from '@mui/x-date-pickers/internals/demo';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import ButtonGroup from '@mui/material/ButtonGroup';
import 'react-time-picker/dist/TimePicker.css';
import 'react-clock/dist/Clock.css';
// Define the props in case you need to customize labels or add more props in the future
interface LeftColumnProps {
  labelImageSet:Function;
  unlabeledSet:Function;
  imageToDownload:string;
  setLabels:Function;
}


const LeftColumn: React.FC<LeftColumnProps> = ({ labelImageSet,unlabeledSet,imageToDownload,setLabels }) => {
  const [latVal,setLatVal] = useState("34-52-11.44N")
  const [lonVal,setLonVal] = useState("6-58-29.82E")
  const [timeVal,setTimeVal] = useState("10:00AM")
  const [dateVal,setDateVal] = useState(dayjs())
  const [dateString,setDateString] = useState(dayjs().format("MM/DD/YYYY"))
  //checks to make sure user entered latitude in correct format
  const handleLatChange=(val:string)=>{
    //check if latitude is in correct format with regular expression
    const latRegex = new RegExp(/\d{1,3}-\d{1,3}-\d{1,3}.\d{1,3}(N|S)/gm)
    if(latRegex.test(val)){
      setLatVal(val)
    }
    else{
      console.error("incorrect format! Try again!")
      setLatVal("")
    }
  }
  const handleLongChange=(val:string)=>{
    //check if longitude is in correct format with regular expression
    const latRegex = new RegExp(/\d{1,3}-\d{1,3}-\d{1,3}.\d{1,3}(E|W)/gm)
    if(latRegex.test(val)){
      setLonVal(val)
    }
    else{
      console.log("incorrect format!")
      setLonVal("")
    }
  }
  const handleTimeValChange=(val: string | null)=>{
    //check for null
    if(val){
      //converting time from 24 hour format to 12 hour format
      //split time into hours and min
      let timeOfDay = ""
      let timeParts = val.split(":")
      //get hours as integer
      let intVal = parseInt(timeParts[0])
      //if past noon, we are in the PM time
      if(intVal>12){
        //convert to 12 hour format
        intVal -=12
        timeOfDay="PM"
      }
      else{
        timeOfDay="AM"
      }
      //construct 12 hour time string, format HH:MM AM/PM
      const newDate = `${intVal}:${timeParts[1]}${timeOfDay}`
      setTimeVal(newDate) 
    }
  }
  const handleDateChange=(val:Dayjs|null)=>{
    if(val){
      setDateVal(val)
      setDateString(val.format('MM/DD/YYYY'))

    }
  }
  //post data to server
  function generateStarMap(){
    axios.post('http://localhost:5000/getStarData', {

    lat: latVal,
    lon: lonVal,
    date: dateString,
    time: timeVal,
    
  })
  .then((response: any)=>{

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
    <div style={{ width: '200%', float: 'left', padding: '10px', textAlign: 'center', fontFamily: 'monospace', fontSize: '25px' }}> {/* Adjust the styling as needed */}
        <div style={{ marginBottom: '20px' }}>
        <label>Latitude (Format: DDD-DDD-DD.DD[N|S])</label>
        <TextField label="Latitude" value={latVal} onChange={(e)=>{handleLatChange(e.target.value)}} style={{height: '5vh', width: '100%' ,  padding: '2px', fontFamily: 'monospace', fontSize: '15px' }}>Latitude</TextField>
        </div>
        <div style={{marginBottom:'20px'}}>
        <label>Longitude (Format: DDD-DDD-DD.DD[E|W]</label>
        <TextField label="Longitude" value={lonVal} onChange={(e)=>{handleLongChange(e.target.value)}} style={{height: '5vh', width: '100%', padding: '2px', fontFamily: 'monospace', fontSize: '15px' }}>Longitude</TextField>
        </div>
        <div style={{ marginBottom: '20px' }}>
        <label>Clock Time</label>
        <TimePicker value={timeVal} onChange={(e)=>{handleTimeValChange(e)}}></TimePicker>
        </div>
        <div style={{ marginBottom: '20px' }}>
        <label>Date:</label>
        <LocalizationProvider dateAdapter={AdapterDayjs}>
      <DemoContainer components={['DatePicker']}>
        <DatePicker
          
          label="Date of viewing"
          value={dateVal}
          onChange={(newValue) => handleDateChange(newValue)}
        />
      </DemoContainer>
    </LocalizationProvider>
        </div>
        <ButtonGroup variant="contained" aria-label="Star Map Options">
        <Button buttonStyle={{ color: 'gray', rounded: 'lg', size: 'md' }} onClick={generateStarMap}>
        Map it!
     </Button>
     <Button buttonStyle={{ color: 'gray', rounded: 'lg', size: 'md' }} onClick={downloadImage}>
      Download Current Map
      </Button>
      <Button buttonStyle={{ color: 'gray', rounded: 'lg', size: 'md' }} onClick={()=>setLabels}>
        Toggle Labels
     </Button>
     </ButtonGroup>
    </div>
  );
};

export default LeftColumn;

/* <button style={{padding: '8px 16px', marginTop: '10px', color: 'white', borderRadius: '10px', height: '20px', }}>
        Enter
      </button> */