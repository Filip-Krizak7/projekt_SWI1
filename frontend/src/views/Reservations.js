import React, { useState, useEffect } from "react";
import UserData from "../components/UserData";
import { useNavigate, Link } from "react-router-dom";
import AlternateEmailIcon from "@mui/icons-material/AlternateEmail";
import {
  CONSTANT,
  setMessage,
  resetMessage,
  checkLoginFromNonLogin,
} from "./../CONSTANT";
import "./../css/Reservations.css";
import axios from "axios";

export default function Reservations() {
  const { session, setSession } = React.useContext(UserData);
  let navigate = useNavigate();
  useEffect(() => {
    if (checkLoginFromNonLogin()) {
      navigate("/");
    }
  }, []);

  useEffect(() => {
    if (session.access_token !== "") {
      myReservations();
    }
  }, [session]);

  const [hotels, setHotels] = useState([]);

  const myReservations = async () => {
    const headers = {
      Authorization: `Bearer ${session.access_token}`,
    };
    await axios
      .get(CONSTANT.server + "reservation/show", { headers })
      .then((responce) => {
        let res = responce.data;
        if (responce.status === 200) {
          setHotels(res);
        }
      })
      .catch((error) => {
        setMessage(error.response.data.detail, "danger");
        console.log(error.response.data.detail);
      });
  };

  const cancelReservation = async (e, _id) => {
    const headers = {
      Authorization: `Bearer ${session.access_token}`,
    };
    await axios
      .delete(CONSTANT.server + `reservation/cancel/${_id}`, { headers })
      .then((responce) => {
        let res = responce.data;
        if (responce.status === 200) {
          myReservations();
        }
      })
      .catch((error) => {
        setMessage(error.response.data.detail, "danger");
        console.log(error.response.data.detail);
      });
  };
  return (
    <div className="__Reservations">
      <div className="text">
        <h1>My Reservations</h1>
      </div>
      {hotels.length > 0 ? (
        <div className="content mt-5 mb-5">
          <div className="row w-100">
            {hotels.map((hotel, index) => {
              return (
                <div
                  className="col-lg-4 col-md-6 col-sm-12 mt-4 mb-4"
                  key={index}
                >
                  <div className="card w-100">
                    <div className="card-body w-100">
                      {hotel.name ? (
                        <span className="custom-card-name mb-3">
                          {hotel.name}
                        </span>
                      ) : null}
                      {hotel.address ? (
                        <span className="custom-card-address mb-1">
                          <span className="text-muted">Address : </span>
                          {hotel.address}
                        </span>
                      ) : null}
                      {hotel.roomType ? (
                        <span className="custom-card-address mb-1">
                          <span className="text-muted">Room Type : </span>
                          {hotel.roomType}
                        </span>
                      ) : null}
                      {hotel.persons ? (
                        <span className="custom-card-address mb-1">
                          <span className="text-muted">Persons : </span>
                          <span className="c-bold">{hotel.persons}</span>
                        </span>
                      ) : null}
                      {hotel.price ? (
                        <span className="custom-card-address mb-1">
                          <span className="text-muted">Price : </span>
                          <span className="c-bold">{hotel.price}</span>
                        </span>
                      ) : null}
                      {hotel.checkIn ? (
                        <span className="custom-card-address mt-4 mb-1">
                          <span className="text-muted">Check In : </span>
                          <span className="c-bold">{hotel.checkIn}</span>
                        </span>
                      ) : null}
                      {hotel.checkOut ? (
                        <span className="custom-card-address mb-1">
                          <span className="text-muted">Check Out : </span>
                          <span className="c-bold">{hotel.checkOut}</span>
                        </span>
                      ) : null}

                      <div className="w-100 mt-1 custom-button">
                        <button
                          type="button"
                          className="btn btn-primary"
                          style={{
                            padding: "12px 15px",
                          }}
                          onClick={(e) => {
                            cancelReservation(e, hotel._id);
                          }}
                        >
                          Cancel Reservation
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      ) : (
        <span>No Reservations</span>
      )}
    </div>
  );
}
