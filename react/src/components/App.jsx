import React, { Fragment, useState, useEffect, useContext } from "react";
import { AppContext } from "../contexts/AppContext";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import withStyles from "@material-ui/core/styles/withStyles";
import AppBar from "@material-ui/core/AppBar";
import Toolbar from "@material-ui/core/Toolbar";
import Typography from "@material-ui/core/Typography";
import Paper from "@material-ui/core/Paper";
import _ from "lodash";
import MessageBar from "./MessageBar";
import Iframe from "react-iframe";

const styles = theme => ({
  App: {
    textAlign: "center",
    alignContent: "center"
  },
  grow: {
    flexGrow: 1
  },
  iframeContainer: {
    border: 0,
    width: "100%",
    height: 500,
    left: 0,
    top: 0,
    position: "absolute"
  },
  content: {
    textAlign: "center",
    alignContent: "center"
  }
});

const App = ({ classes }) => {
  const { message } = useContext(AppContext);

  useEffect(() => {
    console.log("Mount: App");
    return () => {
      console.log("Unmount: App");
    };
  }, []);
  return (
    <Router>
      <div className={classes.App}>
        <AppBar position="static">
          <Toolbar>
            <Typography variant="h6" color="inherit" className={classes.grow}>
              Job Controller 
            </Typography>
          </Toolbar>
        </AppBar>
        <Paper width={1} className={classes.content} elevation={0}>
          <Switch>
            <Route exact path="/">
              Hello React 
            </Route>
          </Switch>
        </Paper>
        {message ? <MessageBar /> : null}
      </div>
    </Router>
  );
};

export default withStyles(styles)(App);
