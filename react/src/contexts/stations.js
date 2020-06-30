import { useState, useEffect } from "react";
import axios from "axios";

// WEB API route for stations
const routeStations = "/stations";

//-------------------------------------------
// Supporting functions
//-------------------------------------------

// Get list of stations
const getStationsList = async (setMessage, setSationsList) => {
  console.log("getStationsList");
  await axios
    .get(routeStations)
    .then(response => {
      console.log("Got stations. setStationList");
      console.log(response.data);
      setSationsList(response.data);
    })
    .catch(error => {
      const error_text = error.response.data.msg;
      const msg = "Error Fetch List: " + error_text;
      setMessage({ variant: "error", content: msg });
    });
};

// Update one elemnet of the list
const onStationsListEdit = (setMessage, changeset) => {
  console.log("onStationsListEdit");
  console.log("changeset: " + JSON.stringify(changeset));
  // Check for emtpy values
  if (
    !changeset.id ||
    !changeset.StationID ||
    !changeset.JobType ||
    !changeset.ManufacturingSite ||
    !changeset.NetToSerialMac
  ) {
    const msg = "ERROR: Reject Edit: Empty fields";
    setMessage({ variant: "error", content: msg });
    return;
  }
  // Commit change to server
  axios
    .put(routeStations + "/" + changeset.id, changeset)
    .then(() => {
      const msg = "Station Edit Successful";
      setMessage({ variant: "success", content: msg });
    })
    .catch(error => {
      const error_text = error.response;
      const msg = "Station Add Failed: " + error_text;
      setMessage({ variant: "error", content: msg });
    });
};

// Delete one elemnet from the list
const onStationsListRemove = (setMessage, changeset) => {
  console.log("onStationsListRemove");
  console.log("changeset: " + JSON.stringify(changeset));
  axios
    .delete(routeStations + "/" + changeset.id)
    .then(() => {
      const msg = "Station Remove Successful";
      setMessage({ variant: "success", content: msg });
    })
    .catch(error => {
      const error_text = error.toString();
      const msg = "Station Removed Failed: " + error_text;
      setMessage({ variant: "error", content: msg });
    });
};

// Add one elemnet to the list
const onStationsListAdd = (setMessage, changeset) => {
  console.log("onStationsListAdd");
  // ensure proper fields
  for (const [key, value] of Object.entries(changeset)) {
    console.log(`${key}: ${value}`);
    // Using == compared to null to detect both null and undefined
    if (`${value}` == null || `${value}` === "") {
      const msg = "ERROR: Reject Empty fields: " + key;
      setMessage({ variant: "error", content: msg });
      return;
    }
  }
  // Commit change to server
  axios
    .post(routeStations, changeset)
    .then(() => {
      const msg = "Station Add Successful";
      setMessage({ variant: "success", content: msg });
    })
    .catch(error => {
      const msg = "ERROR: Reject Empty fields: " + error.response;
      setMessage({ variant: "error", content: msg });
    });
};

//-------------------------------------------
// Hook Usage:
// import { useStations } from "./stations.js";
// const statons = useStations();
// console.log(statons.stationsList);
// stations.refresh();
// stations.add(<changeset>);
// stations.remove(<changeset>);
// stations.update(<changeset>);
//-------------------------------------------
const useStations = setMessage => {
  const [stationsList, setSationsList] = useState([]);

  // On mount get the list
  useEffect(() => {
    getStationsList(setMessage, setSationsList);
  }, []);

  // After each operation, refresh the list
  const refresh = () => {
    getStationsList(setMessage, setSationsList);
  };
  // Basic functions
  const add = changeset => {
    onStationsListAdd(setMessage, changeset);
    refresh();
  };
  const remove = changeset => {
    onStationsListRemove(setMessage, changeset);
    refresh();
  };
  const update = changeset => {
    onStationsListEdit(setMessage, changeset);
    refresh();
  };

  return {
    stationsList,
    refresh,
    add,
    remove,
    update
  };
};
export { useStations };
