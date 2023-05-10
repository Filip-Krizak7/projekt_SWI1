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
import DialogActions from "@mui/material/DialogActions";
import Dialog from "@mui/material/Dialog";
import DialogContent from "@mui/material/DialogContent";
import DialogTitle from "@mui/material/DialogTitle";
import Rating from "@mui/material/Rating";

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
  const [open3, setOpen3] = useState(false);
  const [description, setDescription] = useState("");
  const [ratingValue, setRatingValue] = useState();
  const [reviewId, setReviewId] = useState();
  const [hotelName, setHotelName] = useState("");
  const [userNameGet, setUserNameGet] = useState();
  const [errors, setErrors] = useState({
    description: null,
    rating: null,
  });


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

  const handleClose3 = () => {
    setOpen3(false);
    setReviewId();
  };
  const handleReview = (e, name) => {
    setHotelName(name);
    setOpen3(true);
  };

  const validateSubmit = (e) => {
    e.preventDefault();
    const tempErrors = {
      description: !description && "Please Enter Comments",
      rating: !ratingValue && "Please Enter Rating",
    };
    setErrors(tempErrors);
    if (Object.values(tempErrors).filter((value) => value).length) {
      // console.log(
      //   "..values",
      //   Object.values(tempErrors).filter((value) => value)
      // );
      return;
    }
    handleSubmitRating();
  };

  const handleSubmitRating = async () => {
    const headers = {
      Authorization: `Bearer ${session.access_token}`,
    };

    const formData = new FormData();

    formData.append("text", description);
    formData.append("rating", ratingValue);

    if (reviewId) {
      await axios
        .put(CONSTANT.server + `review/${reviewId}?id=${reviewId}&text=${description}&rating=${ratingValue}`, {}, { headers })
        .then((responce) => {
          let res = responce.data;
          if (responce.status === 200) {
            // setHotels(res);
            setOpen3(false);
            setReviewId();
            myReservations();
          }
        })
        .catch((error) => {
          setMessage(error.response.data.detail, "danger");
          console.log(error.response.data.detail);
        });
    } else {
      await axios
        .post(
          CONSTANT.server +
            `review/create/${hotelName}/${description}/${ratingValue}`,
          {},
          { headers }
        )
        .then((responce) => {
          let res = responce.data;
          if (responce.status === 200) {
            // setHotels(res);
            setOpen3(false);
            setReviewId();
            myReservations();
          }
        })
        .catch((error) => {
          setMessage(error.response.data.detail, "danger");
          console.log(error.response.data.detail);
        });
    }
  };

  useEffect(() => {
    const storedData = window.sessionStorage.getItem("loggedin");
    if (storedData) {
      setUserNameGet(JSON.parse(storedData));
    }
  }, []);

  const handleEditRating = (e, id, rating, Comment) => {
    setReviewId(id);
    setDescription(Comment);
    setRatingValue(rating);
    setOpen3(true);
  };

  const handleDeleteRating = async (e, _id) => {
   
      const headers = {
        Authorization: `Bearer ${session.access_token}`,
      };
      await axios
        .delete(CONSTANT.server + `review/cancel/${_id}`, { headers })
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
                    <span className="rating">
                      {hotel.review ? (
                        <>
                            <Rating
                              readOnly
                              name="simple-controlled"
                              value={hotel.review.rating}
                            />
                              <div className="Editicon">
                            <span>
                              <i
                                className="material-icons editconsRating"
                                onClick={(e) => {
                                  handleEditRating(
                                    e,
                                    hotel.review.id,
                                    hotel.review.rating,
                                    hotel.review.text
                                  );
                                }}
                              >
                                edit
                              </i>
                            </span>
                            <span>
                              <i onClick={(e)=>{
                                handleDeleteRating(e,hotel.review.id)
                              }} className="material-icons delteicons">delete</i>
                            </span>
                          </div>
                        
                        
                        </>
                      ) : (
                        <div className="add-btnratingb">
                        <button
                          className="addratingbutton"
                          onClick={(e) => {
                            handleReview(e, hotel.name);
                          }}
                        >
                          Add Rating
                        </button>
                        </div>
                      )}
                      </span>
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

                      {hotel.review ? (
                        <span className="custom-card-address mb-1">
                          <span className="text-muted">Comments : </span>
                          <span className="c-bold">{hotel.review.text}</span>
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
          <Dialog
            className="profileImgDialognew"
            open={open3}
            onClose={handleClose3}
          >
            <DialogTitle className="profileImgHeading">
              Review
              <span onClick={handleClose3}>
                <i className="fa-solid fa-xmark"></i>
              </span>
            </DialogTitle>
            <div className="dialogcontent_and_actionsinvite">
              <DialogContent className="image_and_namesinvite">
                <div className="Topallpage-- AllPageHight--">
                  <div className="invitepage2">
                    <div className="invite1sec">
                      <div className="hotelnameDiv">
                        {hotelName ? (
                          <span className="custom-card-name mb-3">
                            {hotelName}
                          </span>
                        ) : null}
                      </div>

                      <div className="ratingData">
                        <span className="ratingName">Rating :</span>
                        <Rating
                          name="simple-controlled"
                          value={ratingValue}
                          onChange={(event, newValue) => {
                            setRatingValue(newValue);
                            setErrors({ ...errors, rating: null });
                          }}
                        />
                        <span
                          className="Ag_E"
                          style={{
                            color: "#D14F4F",
                            opacity: errors.rating ? 1 : 0,
                          }}
                        >
                          {errors.rating ?? "valid"}
                        </span>
                      </div>
                      <div
                        className={
                          errors.description
                            ? "text-content addjobtopdiv  error Describe_4"
                            : "text-content addjobtopdiv  Describe_4"
                        }
                      >
                        <h4 className="Describetext_agency_text">Comments :</h4>
                        <textarea
                          className="w-551 border-1 border-radius h-180 Textbox-textarea bkC2"
                          placeholder=""
                          maxLength={2000}
                          value={description}
                          onChange={(e) => {
                            setDescription(e.target.value);
                            setErrors({ ...errors, description: null });
                          }}
                        />
                        <p className="deslimtsec_4">
                          <span
                            style={{
                              color: description?.length === 2000 && "#D14F4F",
                            }}
                          >
                            {description?.length ?? 0}
                            /2000
                          </span>
                        </p>

                        <span
                          className="Ag_E"
                          style={{
                            color: "#D14F4F",
                            opacity: errors.description ? 1 : 0,
                          }}
                        >
                          {errors.description ?? "valid"}
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
              </DialogContent>
            </div>
            <DialogActions>

              <button
                onClick={handleClose3}
                className="create-account-btn mt-2 border-radius CancelAddBtN workflowcancelbtn addeditbtninvitcancel"
              >
                Cancel
              </button>
              <button
                onClick={validateSubmit}
                type="button"
                className="btn-primary Small border-radius mt-2 addeditbtn addeditbtninvitesave"
              >
                Submit
              </button>
            </DialogActions>
          </Dialog>
        </div>
      ) : (
        <span>No Reservations</span>
      )}
    </div>
  );
}
