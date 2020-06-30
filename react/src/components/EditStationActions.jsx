import React, { useEffect, useState, useContext } from "react";
import { withStyles } from "@material-ui/core/styles";
import EditIcon from "@material-ui/icons/Edit";
import DeleteIcon from "@material-ui/icons/Delete";
import CancelIcon from "@material-ui/icons/Cancel";
import ConfirmIcon from "@material-ui/icons/CheckCircle";
import Tooltip from "@material-ui/core/Tooltip";
import Button from "@material-ui/core/Button";
import FormControl from "@material-ui/core/FormControl";
import FormGroup from "@material-ui/core/FormGroup";
import { ListItem } from "@material-ui/core";
import EditStationElements from "./EditStationElements";
import { AppContext } from "../contexts/AppContext";

const styles = theme => ({
  margin: {
    margin: theme.spacing(1)
  },
  confirmChange: {
    color: "#4caf50",
    fontFamily: "Verdana, Arial, Helvetica, sans-serif",
    fontSize: "20px"
  },
  cancelChange: {
    color: "#f44336",
    fontFamily: "Verdana, Arial, Helvetica, sans-serif",
    fontSize: "20px"
  },
  removeStation: {
    color: "#f44336",
    fontFamily: "Verdana, Arial, Helvetica, sans-serif",
    fontSize: "20px"
  },
  changeStation: {
    color: "#4caf50",
    fontFamily: "Verdana, Arial, Helvetica, sans-serif",
    fontSize: "20px"
  }
});

const EditStationActions = ({
  classes,
  item,
  actionName,
  setShowAddButton
}) => {
  const { stations } = useContext(AppContext);
  const [newStationID, setNewStationID] = useState(
    item.StationID
  );
  const [newJobType, setNewJobType] = useState(
    item.JobType
  );
  const [newManufacturingSite, setNewManufacturingSite] = useState(
    item.ManufacturingSite
  );
  const [newNetToSerialMac, setNewNetToSerialMac] = useState(
    item.NetToSerialMac
  );
  const [actionConfirmName, setActionConfirmName] = useState(actionName);

  useEffect(() => {
    console.log("Mount: EditStationActions");
    return () => {
      console.log("Unmount: EditStationActions");
    };
  }, []);

  const handleRemoveCicked = item => {
    setActionConfirmName("Remove");
    console.log("handleRemoveCicked");
    console.log(JSON.stringify(item));
  };
  const handleEditCicked = item => {
    setActionConfirmName("Edit");
    console.log("handleEditCicked");
    console.log(JSON.stringify(item));
  };
  const handleCancelClicked = item => {
    console.log("handleCancelClicked, action: " + actionConfirmName);
    if (actionConfirmName === "Add") {
      console.log("Cancel Add");
      setShowAddButton();
    } else if (actionConfirmName === "Edit") {
      console.log("Cancel Edit");
    } else if (actionConfirmName === "Remove") {
      console.log("Cancel Remove");
    }
    console.log(JSON.stringify(item));
    // Clear the Canceled action
    setActionConfirmName("");
  };
  const handleConfirmClicked = item => {
    console.log("handleConfirmClicked, action:" + actionConfirmName);
    if (actionConfirmName == "Add") {
      console.log(
        ", StationID:" +
          newStationID +
          ", JobType:" +
          newJobType +
          ", ManufacturingSite:" +
          newManufacturingSite +
          ", NetToSerialMac:" +
          newNetToSerialMac
      );
      stations.add({
        StationID: newStationID,
        JobType: newJobType,
        ManufacturingSite: newManufacturingSite,
        NetToSerialMac: newNetToSerialMac
      });
      setShowAddButton();
    } else if (actionConfirmName === "Edit") {
      console.log("Confirm Edit");
      stations.update({
        id: item.id,
        StationID: newStationID,
        JobType: newJobType,
        ManufacturingSite: newManufacturingSite,
        NetToSerialMac: newNetToSerialMac
      });
    } else if (actionConfirmName === "Remove") {
      console.log("Confirm Remove");
      stations.remove(item);
    }
    console.log(JSON.stringify(item));
    // Clear the Canceled action
    setActionConfirmName("");
  };

  const handleAddChange = (
    StationID,
    JobType,
    ManufacturingSite,
    NetToSerialMach
  ) => {
    setNewStationID(StationID);
    setNewJobType(JobType);
    setNewManufacturingSite(ManufacturingSite);
    setNewNetToSerialMac(NetToSerialMach);
  };

  // Default display shows Edit or Delete
  if (!actionConfirmName) {
    return (
      <div>
        <FormControl component="fieldset">
          <FormGroup aria-label="position" name="newJob" value="1" row>
            <ListItem>
              <EditStationElements
                id={item.id}
                StationID={item.StationID}
                JobType={item.JobType}
                ManufacturingSite={item.ManufacturingSite}
                NetToSerialMac={item.NetToSerialMac}
                disableEdit={true}
              />
              <Tooltip
                title={<div className={classes.removeStation}>Remove</div>}
                aria-label="Remove"
              >
                <Button
                  size="small"
                  color="secondary"
                  aria-label="Delete"
                  onClick={event => {
                    handleRemoveCicked(item);
                    event.preventDefault();
                  }}
                  type="submit"
                  className={classes.margin}
                >
                  <DeleteIcon />
                </Button>
              </Tooltip>
              <Tooltip
                title={
                  <div
                    style={{
                      color: "lightblue",
                      fontFamily: "Verdana, Arial, Helvetica, sans-serif",
                      fontSize: "20px"
                    }}
                  >
                    Change
                  </div>
                }
                aria-label="Change"
              >
                <Button
                  size="small"
                  color="primary"
                  aria-label="Edit"
                  onClick={event => {
                    handleEditCicked(item);
                    event.preventDefault();
                  }}
                  type="submit"
                  className={classes.margin}
                >
                  <EditIcon />
                </Button>
              </Tooltip>
            </ListItem>
          </FormGroup>
        </FormControl>
      </div>
    );
  } else if (actionConfirmName == "Remove") {
    return (
      <div>
        <FormControl component="fieldset">
          <FormGroup aria-label="position" name="newJob" value="1" row>
            <ListItem>
              <EditStationElements
                id={item.id}
                StationID={item.StationID}
                JobType={item.JobType}
                ManufacturingSite={item.ManufacturingSite}
                NetToSerialMac={item.NetToSerialMac}
                disableEdit={true}
              />
              <Tooltip
                title={<div className={classes.confirmChange}>Confirm</div>}
              >
                <Button
                  size="small"
                  color="primary"
                  aria-label="Confirm"
                  onClick={event => {
                    handleConfirmClicked(item);
                    event.preventDefault();
                  }}
                  type="submit"
                  className={(classes.margin, classes.confirmChange)}
                >
                  <ConfirmIcon />
                </Button>
              </Tooltip>
              <Tooltip
                title={<div className={classes.cancelChange}>Cancel</div>}
              >
                <Button
                  size="small"
                  color="secondary"
                  aria-label="Cancel"
                  onClick={event => {
                    handleCancelClicked(item);
                    event.preventDefault();
                  }}
                  type="submit"
                  className={(classes.margin, classes.cancelChange)}
                >
                  <CancelIcon />
                </Button>
              </Tooltip>
            </ListItem>
          </FormGroup>
        </FormControl>
      </div>
    );
  } else if (actionConfirmName == "Edit") {
    return (
      <div>
        <FormControl component="fieldset">
          <FormGroup aria-label="position" name="newJob" value="1" row>
            <ListItem>
              <EditStationElements
                id={item.id}
                StationID={item.StationID}
                JobType={item.JobType}
                ManufacturingSite={item.ManufacturingSite}
                NetToSerialMac={item.NetToSerialMac}
                onChange={handleAddChange}
                disableEdit={false}
              />
              <Tooltip
                title={<div className={classes.confirmChange}>Confirm</div>}
              >
                <Button
                  size="small"
                  color="primary"
                  aria-label="Confirm"
                  onClick={event => {
                    handleConfirmClicked(item);
                    event.preventDefault();
                  }}
                  type="submit"
                  className={(classes.margin, classes.confirmChange)}
                >
                  <ConfirmIcon />
                </Button>
              </Tooltip>
              <Tooltip
                title={<div className={classes.cancelChange}>Cancel</div>}
              >
                <Button
                  size="small"
                  color="secondary"
                  aria-label="Cancel"
                  onClick={event => {
                    handleCancelClicked(item);
                    event.preventDefault();
                  }}
                  type="submit"
                  className={(classes.margin, classes.cancelChange)}
                >
                  <CancelIcon />
                </Button>
              </Tooltip>
            </ListItem>
          </FormGroup>
        </FormControl>
      </div>
    );
  } else if (actionConfirmName == "Add") {
    return (
      <div>
        <FormControl component="fieldset">
          <FormGroup aria-label="position" name="newJob" value="1" row>
            <ListItem>
              <EditStationElements
                StationID={newStationID}
                JobType={newJobType}
                ManufacturingSite={newManufacturingSite}
                NetToSerialMac={newNetToSerialMac}
                onChange={handleAddChange}
                disableEdit={false}
              />
              <Tooltip
                title={<div className={classes.confirmChange}>Confirm</div>}
              >
                <Button
                  size="small"
                  color="primary"
                  aria-label="Confirm"
                  onClick={event => {
                    handleConfirmClicked(item);
                    event.preventDefault();
                  }}
                  type="submit"
                  className={(classes.margin, classes.confirmChange)}
                  disabled={
                    newStationID === "" ||
                    newJobType === "" ||
                    newManufacturingSite === "" ||
                    newNetToSerialMac === ""
                  }
                >
                  <ConfirmIcon />
                </Button>
              </Tooltip>
              <Tooltip
                title={<div className={classes.cancelChange}>Cancel</div>}
              >
                <Button
                  size="small"
                  color="secondary"
                  aria-label="Cancel"
                  onClick={event => {
                    handleCancelClicked(item);
                    event.preventDefault();
                  }}
                  type="submit"
                  className={(classes.margin, classes.cancelChange)}
                >
                  <CancelIcon />
                </Button>
              </Tooltip>
            </ListItem>
          </FormGroup>
        </FormControl>
      </div>
    );
  } else {
    return <div>Unknon Action: {actionConfirmName}</div>;
  }
};

export default withStyles(styles)(EditStationActions);
