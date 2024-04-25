'use client'
import { shape } from 'prop-types';
import React from 'react';
import Button from './button';
import axios, { isCancel, AxiosError } from 'axios';
import TimePicker from 'react-time-picker';
import { Box, TextField, Grid } from '@mui/material';
import dayjs, { Dayjs } from 'dayjs';
import { useState } from 'react';
import { DemoContainer } from '@mui/x-date-pickers/internals/demo';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import 'react-time-picker/dist/TimePicker.css';
import 'react-clock/dist/Clock.css';
// The Left Column component requires the state setters for both possible star map images (labeled and unlabeled), the current image to download should the user request it,
// and the state setter for if labels are to be shown on the star map
interface LeftColumnProps {
  labelImageSet: Function;
  unlabeledSet: Function;
  imageToDownload: string;
  setLabels: Function;
}


const LeftColumn: React.FC<LeftColumnProps> = ({ labelImageSet, unlabeledSet, imageToDownload, setLabels }) => {
  const [latVal, setLatVal] = useState("34-52-11.44N")
  const [lonVal, setLonVal] = useState("6-58-29.82E")
  const [timeVal, setTimeVal] = useState("10:00")
  const [dateVal, setDateVal] = useState(dayjs())
  const [dateString, setDateString] = useState(dayjs().format("MM/DD/YYYY"))
  //checks to make sure user entered latitude in correct format
  const checkLat = (val: string) => {
    //check if latitude is in correct format with regular expression
    const latRegex = new RegExp(/\d{1,3}-\d{1,2}-\d{1,2}.\d{1,2}(N|S)/gm)
    //if true, format is correct! 
    if (latRegex.test(val)) {
      return true
    }
    //incorrect format entered, reset input and prompt to try again
    else {
      console.error("incorrect format! Try again!")
      setLatVal("")
      return false
    }
  }
  //verifies longitude is in correct format 
  const checkLon = (val: string) => {
    //check if longitude is in correct format with regular expression
    const latRegex = new RegExp(/\d{1,3}-\d{1,2}-\d{1,2}.\d{1,2}(E|W)/gm)
    //if true, format is correct! 
    if (latRegex.test(val)) {
      return true
    }
    //incorrect format entered, reset input and prompt to try again
    else {
      console.log("incorrect format!")
      setLonVal("")
      return false
    }
  }
  const handleTimeValChange = (val: string | null) => {
    //check for null
    if (val) {
      //converting time from 24 hour format to 12 hour format
      //split time into hours and min
      let timeOfDay = ""
      let timeParts = val.split(":")
      //get hours as integer
      let intVal = parseInt(timeParts[0])
      //if past noon, we are in the PM time
      if (intVal > 12) {
        //convert to 12 hour format
        intVal -= 12
        timeOfDay = "PM"
      }
      else {
        //0:00 is actually midnight (12 AM)
        if(intVal==0){
          intVal=12
        }
        timeOfDay = "AM"
      }
      //construct 12 hour time string, format HH:MM AM/PM
      const newDate = `${intVal}:${timeParts[1]}${timeOfDay}`
      return newDate
    }
  }
  //set date used by MUI date picker, and the date string we will be sending to the backend
  const handleDateChange = (val: Dayjs | null) => {
    if (val) {
      setDateVal(val)
      setDateString(val.format('MM/DD/YYYY'))

    }
  }
  const handleLabels=() =>{
    setLabels()
  }
  //post data to server
  function generateStarMap() {
    if(checkLat(latVal) && checkLon(lonVal)){
      let formattedTime = handleTimeValChange(timeVal)
      axios.post('http://localhost:5000/getStarData', {

      lat: latVal,
      lon: lonVal,
      date: dateString,
      time: formattedTime,

    })
      .then((response: any) => {
        //set both labeled and unlabeled images 
        let imageToDisplay = "data:image/png;base64," + response.data[0]
        unlabeledSet(imageToDisplay)
        imageToDisplay = "data:image/png;base64," + response.data[1]
        labelImageSet(imageToDisplay)
        //reset user input
        setLatVal("")
        setLonVal("")
        setDateVal(dayjs())
        setDateString(dayjs().format('MM/DD/YYY'))
        setTimeVal("10:00AM")

      })
      .catch((err:any)=>{
        console.error(`Request failed with the following error: ${err}`)
      })

    }

  }
  //downloads current star map a png
  function downloadImage() {
    var a = document.createElement("a"); //Create <a>
    a.href = imageToDownload; //Image Base64 Goes here
    a.download = "StarMap.png"; //File name Here
    a.click(); //Downloaded file
  }
  return (
    <Box sx={{ flexGrow: 1 }}>
      <Grid container spacing={2}>
        <Grid item xs={10}>
          <div style={{ marginBottom: '20px' }}>
            <TextField label="Latitude" value={latVal} onChange={(e) => { setLatVal(e.target.value) }} style={{ height: '5vh', width: '100%', padding: '2px', fontFamily: 'monospace', fontSize: '15px',marginBottom:'10px' }}>Latitude</TextField>
            <label>Format: DDD-MM-SS.SS[N|S]</label>
          </div>
        </Grid>
        <Grid item xs={10}>
          <div style={{ marginBottom: '20px' }}>
            <TextField label="Longitude" value={lonVal} onChange={(e) => { setLonVal(e.target.value) }} style={{ height: '5vh', width: '100%', padding: '2px', fontFamily: 'monospace', fontSize: '15px',marginBottom:'10px' }}>Longitude</TextField>
            <label>Format: DDD-MM-SS.SS[N|S]</label>
          </div>
        </Grid>
        <Grid item xs={10}>
          <div style={{ marginBottom: '20px' }}>
            <label>Clock Time</label>
            <TimePicker value={timeVal} onChange={(e) => { setTimeVal(e||"10:00") }}></TimePicker>
          </div>
        </Grid>
        <Grid item xs={12}>
          <div style={{ marginBottom: '20px' }}>
            <label>Date:</label>
            <LocalizationProvider dateAdapter={AdapterDayjs}>
              <DemoContainer components={['DatePicker']}>
                <DatePicker
                  value={dateVal}
                  onChange={(newValue) => handleDateChange(newValue)}
                />
              </DemoContainer>
            </LocalizationProvider>
          </div>
        </Grid>
        <Grid item xs={8}>
          <Button buttonStyle={{ color: 'gray', rounded: 'lg', size: 'md' }} onClick={generateStarMap}>
            Map it!
          </Button>
        </Grid>
        <Grid item xs={8}>
          <Button buttonStyle={{ color: 'gray', rounded: 'lg', size: 'md' }} onClick={handleLabels}>
            Toggle Labels
          </Button>
        </Grid>
        <Grid item xs={8}>
          <Button buttonStyle={{ color: 'gray', rounded: 'lg', size: 'md' }} onClick={downloadImage}>
            Download Current Map
          </Button>
        </Grid>
      </Grid>
    </Box>
  );
};

export default LeftColumn;

/* <button style={{padding: '8px 16px', marginTop: '10px', color: 'white', borderRadius: '10px', height: '20px', }}>
        Enter
      </button> */