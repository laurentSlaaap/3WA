import React, { useState } from "react";
import {
  BrowserRouter as Router,
  Switch,
  Redirect,
  Route
} from "react-router-dom";

import "./App.scss";
import { Header } from "./infrastructure/header/header-component";
import { Routes } from "./utils/routes/routes";

import Cookies from "js-cookie";

const AuthApi = React.createContext();
const TokenApi = React.createContext();


function App() {

  const [auth, setAuth] = useState(false);
  const [token, setToken] = useState("");

  const readCookie = () => {
    let token = Cookies.get("token");
    if (token) {
      setAuth(true);
      setToken(token);
    }
  };
  const disconnect = () => {
    setAuth(false);
    Cookies.remove("token");

  }

  React.useEffect(() => {
    readCookie();
  }, []);

  return (
    <>
      <AuthApi.Provider value={{ auth, setAuth }}>
        <TokenApi.Provider value={{ token, setToken }}>
          <Router >
            <div>
              <Header auth={auth} disconnect={disconnect} />
              <Routes AuthApi={AuthApi} />
            </div>
          </Router>
        </TokenApi.Provider>
      </AuthApi.Provider>
    </>
  );
}

export default App;