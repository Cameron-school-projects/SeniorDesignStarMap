
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
              So this is where we can put instructions for user to implement the map it stuff
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

