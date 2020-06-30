import React, { useContext } from "react";
import PropTypes from "prop-types";
import classNames from "classnames";
import { withStyles } from "@material-ui/core/styles";
import Snackbar from "@material-ui/core/Snackbar";
import SnackbarContent from "@material-ui/core/SnackbarContent";
import IconButton from "@material-ui/core/IconButton";
import CheckCircleIcon from "@material-ui/icons/CheckCircle";
import WarningIcon from "@material-ui/icons/Warning";
import ErrorIcon from "@material-ui/icons/Error";
import InfoIcon from "@material-ui/icons/Info";
import CloseIcon from "@material-ui/icons/Close";
import green from "@material-ui/core/colors/green";
import amber from "@material-ui/core/colors/amber";
import { AppContext } from "../contexts/AppContext";

const variantIcon = {
  success: CheckCircleIcon,
  warning: WarningIcon,
  error: ErrorIcon,
  info: InfoIcon
};

const styles = theme => ({
  close: {
    width: theme.spacing(4),
    height: theme.spacing(4)
  },
  success: {
    backgroundColor: green[600],
    border: "solid 1px #a8a8a8 !important",
    borderRadius: "0 !important"
  },
  error: {
    backgroundColor: theme.palette.error.dark,
    border: "solid 1px #a8a8a8 !important",
    borderRadius: "0 !important"
  },
  info: {
    backgroundColor: theme.palette.primary.dark,
    border: "solid 1px #a8a8a8 !important",
    borderRadius: "0 !important"
  },
  warning: {
    backgroundColor: amber[700],
    border: "solid 1px #a8a8a8 !important",
    borderRadius: "0 !important"
  },
  thumb: {
    fontSize: 20
  },
  icon: {
    fontSize: 20
  },
  iconVariant: {
    opacity: 0.9,
    marginRight: theme.spacing(1)
  },
  message: {
    display: "flex",
    alignItems: "center"
  }
});
const MySnackbarContent = ({
  classes,
  className,
  content,
  onClose,
  variant,
  ...other
}) => {
  const Icon = variantIcon[variant];
  //console.log("Listed as other: " + JSON.stringify(other));
  return (
    <SnackbarContent
      className={classNames(classes[variant], className)}
      aria-describedby="message-id"
      message={
        <span id="client-snackbar" className={classes.message}>
          <Icon className={classNames(classes.icon, classes.iconVariant)} />
          {content}
        </span>
      }
      action={[
        <IconButton
          key="close"
          aria-label="Close"
          color="inherit"
          className={classes.close}
          onClick={onClose}
        >
          <CloseIcon className={classes.icon} />
        </IconButton>
      ]}
      {...other}
    />
  );
};

MySnackbarContent.propTypes = {
  classes: PropTypes.object.isRequired,
  className: PropTypes.string,
  message: PropTypes.node,
  onClose: PropTypes.func,
  content: PropTypes.string,
  variant: PropTypes.oneOf(["success", "warning", "error", "info"]).isRequired
};

const MySnackbarContentWrapper = withStyles(styles)(MySnackbarContent);

const MessageBar = ({ classes }) => {
  const { message, setMessage } = useContext(AppContext);

  const onMessageBarClosed = () => {
    console.log("close message bar");
    setMessage("");
  };
  console.log(">>>>>>>>>>>>>message:" + message);
  return (
    <Snackbar
      anchorOrigin={{
        vertical: "top",
        horizontal: "center"
      }}
      open={true}
      autoHideDuration={3000}
      onClose={onMessageBarClosed}
    >
      <MySnackbarContentWrapper
        variant={message.variant}
        className={classes.margin}
        content={message.content}
        onClose={onMessageBarClosed}
      />
    </Snackbar>
  );
};

export default withStyles(styles)(MessageBar);
