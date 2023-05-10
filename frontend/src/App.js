import React, { useState, useEffect } from "react";
import "./App.css";
import { Routes, Route, BrowserRouter as Router } from "react-router-dom";
import Home from "./views/Home";
import Reservations from "./views/Reservations";
import Review from "./views/Review"
import Profile from "./views/Profile";
import Login from "./views/Login";
import Register from "./views/Register";
import Layout from "./components/Layout";

function App(props) {
  return (
    <>
      <Router>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route
            path="/"
            element={
              <Layout>
                <Home />
              </Layout>
            }
          />
          <Route
            path="/reservations"
            element={
              <Layout>
                <Reservations />
              </Layout>
            }
          />
          <Route
            path="/review"
            element={
              <Layout>
                <Review />
              </Layout>
            }
          />
          <Route
            path="/profile"
            element={
              <Layout>
                <Profile />
              </Layout>
            }
          />
          <Route
            path="*"
            element={
              <Layout>
                <Home />
              </Layout>
            }
          />
        </Routes>
      </Router>
    </>
  );
}

export default App;
