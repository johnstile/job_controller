import React, { createContext, useState } from "react";
import { useStations } from "./stations.js";

const AppContext = createContext();

function AppContextProvider({ children }) {
  // Feeds MessageBar
  const [message, setMessage] = useState("");
  // Instantiate hook
  const stations = useStations(setMessage);
  const defaultContext = {
    message,
    setMessage,
    stations
  };

  return (
    <AppContext.Provider value={defaultContext}>{children}</AppContext.Provider>
  );
}

export { AppContext, AppContextProvider };
