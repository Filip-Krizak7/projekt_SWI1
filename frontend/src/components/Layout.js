import React, { useState, useEffect } from "react";
import "./../css/Layout.css";
import { useNavigate, Link } from "react-router-dom";
import UserData from "./UserData";
import { checkLoginFromNonLogin } from "./../CONSTANT";
import Navbar from "./Navbar";
const axios = require("axios");

function Layout(props) {
  let navigate = useNavigate();

  // useEffect(() => {
  //   if (checkLoginFromNonLogin()) {
  //     navigate("/login");
  //   }
  // }, []);

  // set the defaults
  let __init_session = {
    access_token: "",
    personal: {
      username: "",
      full_name: "",
      email: "",
      hashed_pass: "",
      disabled: null,
    },
    isLoggedIn: false,
  };
  const [session, setSession] = useState(__init_session);
  useEffect(() => {
    let sessionData = JSON.parse(sessionStorage.getItem("loggedin"));
    if (sessionData) {
      setSession({
        access_token: sessionData.data.access_token,
        personal: sessionData.data.userdata,
        isLoggedIn: true,
      });
    }
  }, []);
  const value = { session, setSession };
  return (
    <UserData.Provider value={value}>
      <div className="__Layout">
        <Navbar isLoggedIn={session.isLoggedIn} __init_session={__init_session} setSession={setSession}/>
        {props.children}
      </div>
    </UserData.Provider>
  );
}
export default Layout;
