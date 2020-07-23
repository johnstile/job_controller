import React, { Fragment, useContext } from "react";
import TextField from "@material-ui/core/TextField";
import Button from "@material-ui/core/Button";
import Grid from "@material-ui/core/Grid";
import classNames from "classnames";
import { withStyles } from "@material-ui/core/styles";
import PropTypes from "prop-types";
import { AppContext } from "../contexts/AppContext";

const styles = theme => ({
  App: {
    alignContent: "center"
  },
  formStyle: {
    display: "block"
  },
  formControl: {
    margin: theme.spacing(0),
    minWidth: 300,
    textAlign: "center",
    color: theme.palette.text.secondary,
    flexGrow: 1
  }
});

const Login = ({ classes }) => {
  const { auth } = useContext(AppContext);

  return (
    <Fragment>
      <Grid
        container
        spacing={8}
        className={classNames(classes.formStyle)}
        justify="center"
        direction="column"
      >
        <Grid item>Login</Grid>
        <Grid item>
          <form onSubmit={auth.login}>
            <Grid
              container
              spacing={8}
              className={classNames(classes.formStyle)}
              justify="center"
              direction="column"
            >
              <Grid item>
                <TextField
                  className={classes.formControl}
                  id="username"
                  label="username"
                  required
                />
              </Grid>
              <Grid item>
                <TextField
                  className={classes.formControl}
                  id="password"
                  label="password"
                  required
                  type="password"
                  autoComplete="password_current"
                />
              </Grid>
              <Grid item>
                <Button
                  className={"button"}
                  variant="contained"
                  color="primary"
                  type="submit"
                >
                  Login
                </Button>
              </Grid>
            </Grid>
          </form>
        </Grid>
      </Grid>
    </Fragment>
  );
};

Login.propTypes = {
  classes: PropTypes.object.isRequired
};
export default withStyles(styles)(Login);
