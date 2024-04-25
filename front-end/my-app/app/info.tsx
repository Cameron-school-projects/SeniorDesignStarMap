
'use client'

import React, {useState} from 'react';

import HelpOutlineOutlinedIcon from '@mui/icons-material/HelpOutlineOutlined';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogTitle from '@mui/material/DialogTitle';
import IconButton from '@mui/material/IconButton';
import Button from '@mui/material/Button';

const InfoDialog: React.FC = () => {
    // State to manage dialog visibility
    const [open, setOpen] = useState<boolean>(false);
  
    // Function to open dialog
    const handleClickOpen = () => {
      setOpen(true);
    };
  
    // Function to close dialog
    const handleClose = () => {
      setOpen(false);
    };
  
    return (
      <div>
        <IconButton onClick={handleClickOpen} aria-label="info">
          <HelpOutlineOutlinedIcon style={{
            fontSize: '28px'
          }} />
        </IconButton>
        <Dialog open={open} onClose={handleClose}>
          <DialogTitle>Instructions</DialogTitle>
          <DialogContent>
            <DialogContentText>
             In order to generate a star map, this application needs 4 things:<br />
             1) a latitude, in the format of DDD-MM-SS.SS[N|S], where D is degrees, M is minutes, and S is seconds,<br />
             2) a longitude, in the format of DDD-MM-SS.SS[E|W], where D is degrees, M is minutes, and S is seconds,<br />
             3) a clock time, entered in the time picker, or with the clock infographic,<br />
             4) and a date, entered through the calender picker.<br />
             <br />
             Once these are entered, pressing the map it! button will generate a star map for your viewing pleasure.<br /><br />
             The "Toggle Labels" button allows you to change if stars, constellations, and planets have labels. Note: this will also change what version is downloaded.<br />
             Lastly, the download starmap button downloads the starmap onto your personal computer. <br />
             <br />
             Enjoy!
             <br />
             -The Astronomicon

            </DialogContentText>
          </DialogContent>
          <DialogActions>
            <Button onClick={handleClose}>Close</Button>
          </DialogActions>
        </Dialog>
      </div>
    );
  };
  
  export default InfoDialog;

