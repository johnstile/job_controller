import React, { useEffect, Fragment } from "react";
import FormControlLabel from "@material-ui/core/FormControlLabel";
import TextField from "@material-ui/core/TextField";
import { withStyles } from "@material-ui/core/styles";

const styles = theme => ({
  formControl: {
    margin: theme.spacing(1),
    textAlign: "center",
    color: theme.palette.text.secondary,
    backgroundColor: "#FFF",
    labelPlacement: "top"
  },
  formStationID: {
    margin: theme.spacing(0),
    padding: theme.spacing(0),
    maxWidth: 100,
    minWidth: 10
  },
  formJobType: {
    margin: theme.spacing(0),
    padding: theme.spacing(0),
    maxWidth: 100,
    minWidth: 10
  },
  formManufacturingSite: {
    margin: theme.spacing(0),
    padding: theme.spacing(0),
    maxWidth: 150,
    minWidth: 10
  },
  formNetToSerialMac: {
    margin: theme.spacing(0),
    padding: theme.spacing(0),
    maxWidth: 150,
    minWidth: 10
  }
});

const EditStationElements = ({
  classes,
  id,
  StationID,
  JobType,
  ManufacturingSite,
  NetToSerialMac,
  onChange,
  disableEdit
}) => {
  useEffect(() => {
    console.log("Mount: EditStationElements");
    return () => {
      console.log("Unmount: EditStationElements");
    };
  }, []);
  const handleStationIDChange = newStationID => {
    onChange(
      newStationID,
      JobType,
      ManufacturingSite,
      NetToSerialMac
    );
  };
  const handleJobTypeChange = newJobType => {
    onChange(
      StationID,
      newJobType,
      ManufacturingSite,
      NetToSerialMac
    );
  };
  const handleManufacturingSiteChange = newManufacturingSite => {
    console.log("CALLED handleManufacturingSiteChange");
    onChange(
      StationID,
      JobType,
      newManufacturingSite,
      NetToSerialMac
    );
  };
  const handleNetToSerialMacChange = newNetToSerialMac => {
    onChange(
      StationID,
      JobType,
      ManufacturingSite,
      newNetToSerialMac
    );
  };
  return (
    <Fragment>
      <FormControlLabel
        key="StationID"
        control={
          <TextField
            name="StationID"
            defaultValue={StationID}
            disabled={disableEdit}
            className={(classes.formControl, classes.formStationID)}
            required
            onChange={event =>
              handleStationIDChange(event.target.value)
            }
          />
        }
        label="Station S/N"
        labelPlacement="top"
        className={classes.formControl}
      />
      <FormControlLabel
        key="JobType"
        control={
          <TextField
            name="JobType"
            defaultValue={JobType}
            disabled={disableEdit}
            className={(classes.formControl, classes.formJobType)}
            required
            onChange={event => handleJobTypeChange(event.target.value)}
          />
        }
        label="JobType"
        labelPlacement="top"
        className={classes.formControl}
      />
      <FormControlLabel
        key="ManufacturingSite"
        control={
          <TextField
            name="ManufacturingSite"
            defaultValue={ManufacturingSite}
            disabled={disableEdit}
            className={(classes.formControl, classes.formManufacturingSite)}
            required
            onChange={event =>
              handleManufacturingSiteChange(event.target.value)
            }
          />
        }
        label="ManufacturingSite"
        labelPlacement="top"
        className={classes.formControl}
      />
      <FormControlLabel
        key="NetToSerialMac"
        control={
          <TextField
            name="NetToSerialMac"
            defaultValue={NetToSerialMac}
            disabled={disableEdit}
            className={(classes.formControl, classes.formNetToSerialMac)}
            required
            onChange={event => handleNetToSerialMacChange(event.target.value)}
          />
        }
        label="NetToSerialMac"
        labelPlacement="top"
        className={classes.formControl}
      />
    </Fragment>
  );
};

export default withStyles(styles)(EditStationElements);
