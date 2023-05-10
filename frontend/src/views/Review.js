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
import "./../css/Review.css";
import axios from "axios";
import DialogActions from "@mui/material/DialogActions";
import Dialog from "@mui/material/Dialog";
import DialogContent from "@mui/material/DialogContent";
import DialogTitle from "@mui/material/DialogTitle";
import ListItem from "@mui/material/ListItem";
import ListItemText from "@mui/material/ListItemText";
import Rating from "@mui/material/Rating";

export default function Review() {
  const { session, setSession } = React.useContext(UserData);
  let navigate = useNavigate();
  // useEffect(() => {
  //   if (checkLoginFromNonLogin()) {
  //     navigate("/");
  //   }
  // }, []);

  useEffect(() => {
    // if (session.access_token !== "") {
      myReservations();
    // }
  }, [session]);

  const [hotels, setHotels] = useState([]);


  const myReservations = async () => {
    const headers = {
      Authorization: `Bearer ${session.access_token}`,
    };
    await axios
      .get(CONSTANT.server + "review/show/", { headers })
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

  

  return (
    <div className="__Reservations">
      <div className="text">
        <h1>Reviews</h1>
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
                  <div className="card w-100 cardData">
                    <div className="card-body w-100 showCardData">
                      {hotel.hotel_name ? (
                        <span className="custom-card-name mb-1">
                          {hotel.hotel_name}
                        </span>
                      ) : null}
                       {hotel.address ? (
                        <span className="custom-card-address mb-3">
                          <span className="text-muted">Address : </span>
                          {hotel.address}
                        </span>
                      ) : null}
                      {hotel.reviews.length > 0 ? (
                        <span className="custom-card-address mb-1">
                          {hotel.reviews.map((item, index) => {
                            return (
                              <div className="showtheReviewDat">
                                {item.username ? (
                                  <span className="review">
                                    <span className="text-muted">
                                      UserName :{" "}
                                    </span>
                                    {item.username}
                                  </span>
                                ) : null}


                                {item.rating ? (
                                  <span className="review ratingData">
                                    <span className="text-muted">
                                      Rating :{" "}
                                    </span>
                                    <Rating
                                      readOnly
                                      name="simple-controlled"
                                      value={item.rating}
                                    />
                                  </span>
                                ) : null}

                                {item.text ? (
                                  <span className="review">
                                    <span className="text-muted">
                                      Comments :{" "}
                                    </span>
                                    {item.text}
                                  </span>
                                ) : null}

                                <hr/>
                              </div>
                            );
                          })}
                        </span>
                      ) : null}
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      ) : (
        <span>No Reviews</span>
      )}
    </div>
  );
}
