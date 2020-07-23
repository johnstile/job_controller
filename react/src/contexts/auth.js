import { useState, useEffect } from "react";
import axios from "axios";
import Cookies from "js-cookie";
import decode from "jwt-decode";

// WEB API route for auth
const routeAuthLogin = "/V1/login";
const routeAuthCheck = "/V1/auth_check";

//-------------------------------------------
// Supporting functions
//-------------------------------------------
const onLoginSubmit = (event, setAuthUser, setMessage) => {
  // Post login
  axios
    .post(routeAuthLogin, {
      username: event.target.username.value,
      password: event.target.password.value
    })
    .then(response => {
      onLoginSuccess(response, setAuthUser, setMessage);
    })
    .catch(error => {
      setMessage({ variant: "error", content: error.response });
    });

  event.preventDefault();
};

const onLoginSuccess = (response, setAuthUser, setMessage) => {
  const accessToken = response.data.access_token;

  if (!accessToken) {
    setMessage({ variant: "error", content: "No Cookie!" });
    return;
  }
  const validation = isJwtTokenCurrent(accessToken);
  if (!validation.status) {
    setMessage({ variant: "error", content: validation.msg });
    return;
  }

  Cookies.set(
    "access_token",
    accessToken //{ secure: true}
  );

  //
  // QUESTION: How can I make this global, for on server calls.
  //
  axios.defaults.headers.common["Authorization"] = "Bearer " + accessToken;

  getJwtTokenClaims(accessToken, setAuthUser);
};

const getJwtTokenClaims = (token, setAuthUser) => {
  try {
    const decoded = decode(token);
    setAuthUser(decoded.identity);
    console.log(decoded.identity);
    return true;
  } catch (err) {
    return false;
  }
};

const isJwtTokenCurrent = token => {
  try {
    const decoded = decode(token);
    if (decoded.exp < Date.now() / 24) {
      return { status: true, msg: "Token is current" };
    } else {
      return { status: false, msg: "Token is expired" };
    }
  } catch (err) {
    return { status: false, msg: "Token Error!" };
  }
};

const onAuthCheck = (event, setMessage) => {
  axios
    .post(routeAuthCheck)
    .then(response => {
      consol.log("Do Something" + response);
    })
    .catch(error => {
      setMessage({ variant: "error", content: error.response });
    });
  // We do want this to reload the page
  //event.preventDefault();
};

const onLogoutSubmit = (setAuthUser, setMessage) => {
  setAuthUser("");
  Cookies.remove("access_token");
  // QUESTION: dialog sometimes does not appear
  setMessage({ variant: "info", content: "Logged Out" });
};
//-------------------------------------------
// Hook Usage:
// import { useAuth } from "./auth.js";
// const auth = useAuth();
// auth.login();
// auth.logout();
// auth.check();
//-------------------------------------------
const useAuth = setMessage => {
  const [authUser, setAuthUser] = useState("");
  //
  // QUESTION:  When I hvae a cookie, this isn't preventing the login
  //
  useEffect(() => {
    const token = Cookies.get("access_token");
    if (token) {
      const decoded = decode(token);
      const authUser = decoded.identity;
      setAuthUser(authUser);
      console.log(authUser);
    }
  }, []);

  const login = event => {
    onLoginSubmit(event, setAuthUser, setMessage);
  };
  const logout = () => {
    onLogoutSubmit(setAuthUser, setMessage);
  };
  const check = event => {
    onAuthCheck(event);
  };

  return {
    login,
    check,
    logout,
    authUser
  };
};

export { useAuth };
