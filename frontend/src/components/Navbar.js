import React, { useState, useEffect } from "react";
import { useNavigate, Link } from "react-router-dom";
import "./../css/Navbar.css";
// import Footer from "../components/footer.js";
import MenuIcon from "@mui/icons-material/Menu";

const Navbar = (props) => {
  let navigate = useNavigate();
  const logout = () => {
    sessionStorage.removeItem("loggedin");
    props.setSession(props.__init_session);
    navigate("/");
  };
  return (
    <>
      <nav className="navbar navbar-expand-lg __Navbar">
        <Link to="/" className="navbar-brand">
          <img
            className="logo"
            src="https://triptease-website.storage.googleapis.com/2017/092017/09/Booking.com_logo2.png"
          />
        </Link>
        <button
          className="navbar-toggler"
          type="button"
          data-toggle="collapse"
          data-target="#navbarSupportedContent"
          aria-controls="navbarSupportedContent"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <MenuIcon className="icon" />
        </button>
        <div className="collapse navbar-collapse" id="navbarSupportedContent">
          <ul className="navbar-nav mr-auto">
            <li className="nav-item">
              <Link to="/" className="nav-link simple-nav-link active">
                Home
              </Link>
            </li>
          </ul>
          <div className="form-inline my-2 my-lg-0">
            <ul className="navbar-nav mr-auto">
              {!props.isLoggedIn ? (
                <>
                  <li className="nav-item">
                    <Link to="/login" className="Button-Custom-1 black">
                      <span className="content">
                        <span className="type">Log In</span>
                      </span>
                    </Link>
                  </li>
                  <li className="nav-item signup">
                    <Link to="/register" className="Button-Custom-1 white">
                      <span className="content">
                        <span className="type">Register</span>
                      </span>
                    </Link>
                  </li>
                </>
              ) : (
                <>
                  <li className="nav-item">
                    <Link to="/reservations" className="Button-Custom-1 black">
                      <span className="content">
                        <span className="type">Reservations</span>
                      </span>
                    </Link>
                  </li>
                  <li className="nav-item signup">
                    <Link to="/profile" className="Button-Custom-1 white">
                      <span className="content">
                        <span className="type">Profile</span>
                      </span>
                    </Link>
                  </li>
                  <li className="nav-item signup">
                    <button className="Button-Custom-1 white" onClick={logout}>
                      <span className="content">
                        <span className="type">Logout</span>
                      </span>
                    </button>
                  </li>
                </>
              )}
            </ul>
          </div>
        </div>
      </nav>
    </>
  );
};

export default Navbar;

// {/* <Button variant="outline-dark" onClick={() => setShowBugComponent(true)}>
//   Click to test if Sentry is capturing frontend errors! (Should only work in Production)
// </Button> */}
// {/* {showBugComponent && showBugComponent.field.notexist} */}
// {/* <div id="django-background"> LUMNIS </div> */}
// {/* <div id="django-logo-wrapper">  </div>  <div> TESTING </div>  <img alt="Django Negative Logo" src={DjangoImgSrc} />  */}
