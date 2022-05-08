import React, { useState, useEffect } from "react";
import AlternateEmailIcon from "@mui/icons-material/AlternateEmail";
import VpnKeyIcon from "@mui/icons-material/VpnKey";
import "./../css/Login.css";
import axios from "axios";
import { useNavigate, Link } from "react-router-dom";
import { CONSTANT, checkLoginFromLogin } from "./../CONSTANT";

function Login(props) {
  let navigate = useNavigate();

  useEffect(() => {
    if (checkLoginFromLogin()) {
      navigate("/dashboard");
    }
  }, []);

  const __init = {
    username: "",
    password: "",
  };
  const [credentials, setCredentials] = useState(__init);
  const changeCredentials = (e) => {
    setCredentials({
      ...credentials,
      [e.target.name]: e.target.value,
    });
  };

  const login = async (e) => {
    e.target.style.pointerEvents = "none";
    e.target.innerHTML =
      '<div className="spinner-border custom-spin" role="status"><span className="visually-hidden">Loading...</span></div>';
    e.preventDefault();
    resetError();
    if (credentials.password !== "") {
      let bodyFormData = new FormData();
      bodyFormData.append("username", credentials.username);
      bodyFormData.append("password", credentials.password);
      await axios
        .post(CONSTANT.server + "token", credentials, {
          headers: { "Content-Type": "multipart/form-data" },
        })
        .then((responce) => {
          let res = responce.data;
          if (responce.status === 200) {
            sessionStorage.setItem(
              "loggedin",
              JSON.stringify({
                data: res,
              })
            );
            navigate("/");
          }
        })
        .catch((error) => {
          setError(error.response.data.detail);
          console.log(error.response.data.detail);
        });
    } else {
      setError("Please Fill All Fields");
    }
    e.target.style.pointerEvents = "unset";
    e.target.innerHTML = "Log In";
  };

  const setError = (text) => {
    let error = document.getElementById("error");
    error.innerHTML = text;
    error.style.display = "block";
  };

  const resetError = () => {
    let error = document.getElementById("error");
    error.innerText = "";
    error.style.display = "none";
  };

  const isError = () => {
    let error = document.getElementById("error");
    if (error.style.display === "none") {
      return false;
    }
    return true;
  };

  return (
    <>
      <div className="row A__Login" style={{ margin: "0px", padding: "0px" }}>
        <div className="col-lg-6 d-none d-lg-flex flex-column background-custom d-flex justify-content-center align-items-center">
          <img
            src="/signin.svg"
            className="img-fluid mb-3"
            alt="Login illustration"
          />
          <h1>Welcome!</h1>
          <p>Enter your credentials</p>
        </div>
        <div className="col-lg-6 col-sm-12 d-flex justify-content-center align-items-center">
          <div className="form d-flex flex-column justify-content-center align-items-center">
            <h1 className="mb-5">Log In</h1>
            <div>
              <div className="custom-input input-group mb-3">
                <span className="input-group-text">
                  <AlternateEmailIcon />
                </span>
                <input
                  type="text"
                  className="form-control"
                  placeholder="Username"
                  name="username"
                  onChange={changeCredentials}
                  value={credentials.username}
                  onKeyDown={(e) => {
                    if (e.key === "Enter" && e.target.value !== "") {
                      login(e);
                    }
                  }}
                />
              </div>
              <div className="custom-input input-group mb-3">
                <span className="input-group-text">
                  <VpnKeyIcon />
                </span>
                <input
                  type="password"
                  className="form-control"
                  placeholder="Password"
                  name="password"
                  onChange={changeCredentials}
                  value={credentials.password}
                  onKeyDown={(e) => {
                    if (e.key === "Enter" && e.target.value !== "") {
                      login(e);
                    }
                  }}
                />
              </div>
              <p
                className="text-danger p-0 m-0 mb-2"
                id="error"
                style={{ display: "none" }}
              >
                Error
              </p>
              <div className="w-100 mt-1 custom-button">
                <button
                  type="button"
                  className="btn btn-primary"
                  style={{
                    padding: "12px 15px",
                  }}
                  onClick={login}
                >
                  Log In
                </button>
              </div>
              <div className="mt-5 d-flex justify-content-center align-items-center">
                <Link to="/">← Back to Home</Link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}

export default Login;
