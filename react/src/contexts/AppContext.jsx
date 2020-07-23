import React, { createContext, useState } from "react";
import { useStations } from "./stations.js";
import { useAuth } from "./auth.js";

const AppContext = createContext();

function AppContextProvider({ children }) {
  // Feeds MessageBar
  const [message, setMessage] = useState("");
  // Instantiate hook
  const stations = useStations(setMessage);
  const auth = useAuth(setMessage);
  const defaultContext = {
    message,
    setMessage,
    stations,
    auth
  };

  return (
    <AppContext.Provider value={defaultContext}>{children}</AppContext.Provider>
  );
}

export { AppContext, AppContextProvider };
