import React, { Fragment, useState, useEffect, useContext } from "react";
import PropTypes from "prop-types";
import Button from "@material-ui/core/Button";
import { withStyles } from "@material-ui/core/styles";
import Grid from "@material-ui/core/Grid";
import List from "@material-ui/core/List";
import CircularProgress from "@material-ui/core/CircularProgress";
import EditStationActions from "./EditStationActions";
import EditStationsHelp from "./EditStationsHelp";
import { AppContext } from "../contexts/AppContext";

const styles = theme => ({
  formStyle: {
    alignItems: "center",
    alignContent: "center"
  },
  progress: {
    margin: theme.spacing(2)
  },
  sectionAdd: {
    margin: theme.spacing(4)
  }
});

const EditStations = ({ classes }) => {
  const { stations } = useContext(AppContext);
  const [showAddButton, setShowAddButton] = useState(true);
  useEffect(() => {
    console.log("Mount: EditStations");
    return () => {
      console.log("Unmount: EditStations");
    };
  }, []);

  const handleAddClicked = () => {
    console.log("handleAddClicked");
    setShowAddButton(false);
  };

  if (stations.stationsList) {
    return (
      <Fragment>
        <Grid container justify="flex-start">
          <Grid item>
            <EditStationsHelp />
          </Grid>
        </Grid>
        <Grid
          container
          spacing={1}
          className={classes.formStyle}
          justify="center"
        >
          <List>
            {stations.stationsList.map(item => (
              <EditStationActions
                key={item.id}
                item={item}
                actionName=""
              />
            ))}
          </List>
        </Grid>
        <Grid
          container
          spacing={1}
          className={(classes.formStyle, classes.sectionAdd)}
          justify="center"
        >
          {showAddButton ? (
            <Grid item>
              <Button
                variant="contained"
                color="primary"
                type="button"
                onClick={handleAddClicked}
              >
                Add
              </Button>
            </Grid>
          ) : (
            <EditStationActions
              key="new"
              item={("", "")}
              actionName="Add"
              setShowAddButton={() => setShowAddButton(true)}
            />
          )}
        </Grid>
      </Fragment>
    );
  } else {
    return (
      <Fragment>
        Loading Stations List
        <CircularProgress className={classes.progress} size={50} />
      </Fragment>
    );
  }
};

EditStations.propTypes = {
  classes: PropTypes.object.isRequired
};

export default withStyles(styles)(EditStations);
