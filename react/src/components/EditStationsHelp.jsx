import React, { Fragment, useState, useEffect } from "react";
import Button from "@material-ui/core/Button";
import Dialog from "@material-ui/core/Dialog";
import DialogActions from "@material-ui/core/DialogActions";
import DialogContent from "@material-ui/core/DialogContent";
import DialogContentText from "@material-ui/core/DialogContentText";
import DialogTitle from "@material-ui/core/DialogTitle";
import EditIcon from "@material-ui/icons/Edit";
import DeleteIcon from "@material-ui/icons/Delete";
import CancelIcon from "@material-ui/icons/Cancel";
import ConfirmIcon from "@material-ui/icons/CheckCircle";

const DirectionsText = () => (
  <Fragment>
     How to use Edit Stations
    <br />
    <menu>
      Terms:
      <li>StationID: Name of station Station (S/N)</li>
      <li>JobType: Kinds of jobs this host can run</li>
      <li>ManufacturingSite: Unique Manufacturing site Location</li>
      <li>NetToSerialMac: MAC of Station</li>
    </menu>
    <menu>
      Actions:
      <li>
        You can Delete (<DeleteIcon />) or Edit (<EditIcon />) existing stations
      </li>
      <li>You can Add a Station (see button at bottom of the page).</li>
      <li>
        Confirm (<ConfirmIcon />) or Cancle ( <CancelIcon />) each action
      </li>
      <li>All fields are Required</li>
    </menu>
  </Fragment>
);
function EditStationsHelp() {
  const [open, setOpen] = useState(false);
  useEffect(() => {
    console.log("Mount: EditStationsHelp");
    return () => {
      console.log("Unmount: EditStationsHelp");
    };
  }, []);

  function handleClickOpen() {
    setOpen(true);
  }

  function handleClose() {
    setOpen(false);
  }

  return (
    <div>
      <Button variant="outlined" color="primary" onClick={handleClickOpen}>
        Directions
      </Button>
      <Dialog
        open={open}
        onClose={handleClose}
        aria-labelledby="form-dialog-title"
      >
        <DialogTitle id="form-dialog-title">Edit Stations Help</DialogTitle>
        <DialogContent>
          <DialogContentText>
            <DirectionsText />
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={e => handleClose(e)} color="primary">
            Dismiss
          </Button>
        </DialogActions>
      </Dialog>
    </div>
  );
}

export default EditStationsHelp;
