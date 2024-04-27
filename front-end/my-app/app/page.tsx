'use client'

import Image from "next/image";
import LeftColumn from "./leftColumn";
//import mapFrame from "./starmapDisplay";
//import BoxSx from "./boxSection";
import { Box, Grid } from '@mui/material';
import InfoDialog from "./info";
import ImageBox from "./map";
import { useState } from 'react';


//import stars from '../images/starsky.jpg';


export default function Home() {

  const [image, setImage] = useState("")
  const [labeledImage, setLabeledImage] = useState("")
  const [showLabels, setShowLabels] = useState(false)
  //toggles if labels are to be shown 
  const handleLabelSwap = () => {
    setShowLabels(!showLabels)
  }
  //renders labeled/unlabeled map depending on current preference 
  function selectImage() {
    if (showLabels) {
      return (<ImageBox imageUrl={labeledImage} altText="I mean it should be the starmap" />)
    }
    else {
      return (<ImageBox imageUrl={image} altText="I mean it should be the starmap" />)

    }
  }
  return (

    <Box color='black' p={5}>


        <Grid container spacing={3}>

        <Grid item xs={2} > 
        
        <Image src={"./images/Logo.webp"} alt="logo" style={{

        width:'100%',
        height:"100%"

        }}>  </Image>
        
        </Grid>

      <Grid item xs={2}
     border="2px solid #000000"
     borderColor="black"
     borderRadius='8px'
     bgcolor='white'
     height="50%"
      >
      <div className="LeftSideColumn">

          <LeftColumn labelImageSet={setLabeledImage} unlabeledSet={setImage} setLabels={handleLabelSwap} imageToDownload={showLabels ? labeledImage : labeledImage} />

      </div>
  
        {/* popup with helpful information */}
        <InfoDialog />
      </Grid>


      <Grid item xs={10}>

        {selectImage()}

      </Grid>
      </Grid>
    </Box>



    
  
  );
}
