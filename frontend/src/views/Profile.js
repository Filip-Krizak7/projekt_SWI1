import React, {useEffect, useState} from "react";
import UserData from "../components/UserData";
import { useNavigate, Link } from "react-router-dom";
import "./../css/Profile.css";
import {
  CONSTANT,
  setMessage,
  resetMessage,
  checkLoginFromNonLogin,
} from "./../CONSTANT";

export default function Profile() {
  let navigate = useNavigate();
  useEffect(() => {
    if (checkLoginFromNonLogin()) {
      navigate("/");
    }
  }, []);
  const { session, setSession } = React.useContext(UserData);
  return (
    <div className="__Profile">
      <div className="text">
        <h1>Profile Information</h1>
      </div>
      <div className="content mt-5">
        <span><span className="text-muted">Username : </span>{session.personal.username}</span>
        <span><span className="text-muted">Email : </span>{session.personal.email}</span>
        <span><span className="text-muted">Full Name : </span>{session.personal.full_name}</span>
      </div>
    </div>
  );
}
