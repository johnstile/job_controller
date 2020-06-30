import React, { useState, useEffect } from "react";
import withStyles from "@material-ui/core/styles/withStyles";
import { useHistory } from "react-router-dom";
import Menu from "@material-ui/core/Menu";
import MenuItem from "@material-ui/core/MenuItem";
import MenuIcon from "@material-ui/icons/Menu";
import IconButton from "@material-ui/core/IconButton";
const styles = theme => ({
  progress: {
    margin: theme.spacing(2)
  }
});

const AppMenu = ({ classes }) => {
  const [anchorEl, setAnchorEl] = useState(null);
  const [toggle, setToggle] = useState(false);
  const history = useHistory();

  useEffect(() => {
    console.log("Mount: AppMenu");
    return () => {
      console.log("Unmount: AppMenu");
    };
  }, []);
  const handleClick = event => {
    console.log(event);
    setAnchorEl(event.currentTarget);
  };
  const handleClose = () => {
    setAnchorEl(null);
  };

  return (
    <div>
      <IconButton onClick={handleClick} color="inherit" aria-label="Menu">
        <MenuIcon />
      </IconButton>
      <Menu
        id="simple-menu"
        anchorEl={anchorEl}
        keepMounted
        open={Boolean(anchorEl)}
        onClose={handleClose}
      >
        <MenuItem
          onClick={() => {
            handleClose();
            history.push("/edit_stations");
          }}
        >
          Edit Stations
        </MenuItem>
      </Menu>
    </div>
  );
};

export default withStyles(styles)(AppMenu);
