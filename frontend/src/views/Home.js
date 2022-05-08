import React, { useState, useEffect } from "react";
import UserData from "../components/UserData";
import LocationCityIcon from '@mui/icons-material/LocationCity';
import SortIcon from '@mui/icons-material/Sort';
import PriceChangeIcon from '@mui/icons-material/PriceChange';
import BedIcon from '@mui/icons-material/Bed';
import PersonIcon from '@mui/icons-material/Person';
import LayersIcon from '@mui/icons-material/Layers';
import DateRangeIcon from '@mui/icons-material/DateRange';
import {
  CONSTANT,
  setMessage,
  resetMessage,
} from "./../CONSTANT";
import { useNavigate, Link } from "react-router-dom";
import "./../css/Home.css";
import axios from "axios";

export default function Home() {
  let navigate = useNavigate();
  const { session, setSession } = React.useContext(UserData);
  const __init = {
    city: "",
    sortBy: "",
    minPrice: "",
    maxPrice: "",
    rooms: "",
    adults: "",
    children: "",
    maxPages: "",
    start_datetime: "",
    end_datetime: "",
  };
  const [data, setData] = useState(__init);
  const changeData = (e) => {
    setData({
      ...data,
      [e.target.name]: e.target.value,
    });
  };

  const [hotels, setHotels] = useState([]);

  const applyFilters = async (e) => {
    e.target.style.pointerEvents = "none";
    e.target.innerHTML =
      '<div className="spinner-border custom-spin" role="status"><span className="visually-hidden">Loading...</span></div>';
    e.preventDefault();
    resetMessage();
    if (data.city !== "") {
      if (data.sortBy !== "") {
        if (
          data.minPrice !== "" &&
          parseInt(data.minPrice) >= 0 &&
          parseInt(data.minPrice) < parseInt(data.maxPrice)
        ) {
          if (
            data.maxPrice !== "" &&
            parseInt(data.maxPrice) >= 0 &&
            parseInt(data.maxPrice) > parseInt(data.minPrice)
          ) {
            if (
              data.rooms !== "" &&
              parseInt(data.rooms) >= 0 &&
              data.adults !== "" &&
              parseInt(data.adults) >= 0 &&
              data.children !== "" &&
              parseInt(data.children) >= 0
            ) {
              if (data.maxPages !== "" && parseInt(data.maxPages) >= 0) {
                if (
                  data.start_datetime !== "" &&
                  data.start_datetime < data.end_datetime
                ) {
                  if (
                    data.end_datetime !== "" &&
                    data.end_datetime > data.start_datetime
                  ) {
                    await axios
                      .get(
                        CONSTANT.server +
                          `hotel/${data.city}/{maxPages}/${data.sortBy}/${data.minPrice}/${data.maxPrice}/${data.rooms}/${data.adults}/${data.children}?maxPages=${data.maxPages}&start_datetime=${data.start_datetime}&end_datetime=${data.end_datetime}`
                      )
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
                  } else {
                    setMessage(
                      "End Date can't be less than Start Date!",
                      "danger"
                    );
                  }
                } else {
                  setMessage(
                    "Start Date can't be greater than End Date!",
                    "danger"
                  );
                }
              } else {
                setMessage("Max Pages can't be less than zero!", "danger");
              }
            } else {
              setMessage(
                "Number of Rooms/Adults/Children can't be less than zero!",
                "danger"
              );
            }
          } else {
            setMessage(
              "Max Price can't be less than zero or Min Price!",
              "danger"
            );
          }
        } else {
          setMessage(
            "Min Price can't be less than zero or greater than Max Price!",
            "danger"
          );
        }
      } else {
        setMessage("Please Select Sort By!", "danger");
      }
    } else {
      setMessage("Please Fill City!", "danger");
    }
    e.target.style.pointerEvents = "unset";
    e.target.innerHTML = "Apply Filters";
  };

  const makeReservation = async (e, index) => {
    e.target.style.pointerEvents = "none";
    e.target.innerHTML =
      '<div className="spinner-border custom-spin" role="status"><span className="visually-hidden">Loading...</span></div>';
    e.preventDefault();
    resetMessage();
    if (session.isLoggedIn) {
      let hotel = hotels[index];
      const headers = {
        Authorization: `Bearer ${session.access_token}`,
      };
      await axios
        .post(
          CONSTANT.server +
            `reservation/create/${hotel.name}/${hotel.address}/${hotel.price}/${hotel.roomType}/${hotel.persons}?checkIn=${data.start_datetime}&checkOut=${data.end_datetime}`,
          {},
          { headers }
        )
        .then((responce) => {
          let res = responce.data;
          if (responce.status === 200) {
            setMessage(`Reservation for ${hotel.name} Added!`, "success")
          }
        })
        .catch((error) => {
          setMessage(error.response.data.detail, "danger");
          console.log(error.response.data.detail);
        });
    } else {
      setMessage("Not Logged In", "danger");
      navigate("/login");
    }
    e.target.style.pointerEvents = "unset";
    e.target.innerHTML = "Reserved";
  };
  return (
    <div className="__Home">
      <div className="text mb-4 mt-4">
        <p
          className="text-danger p-0 m-0 mb-2"
          id="error"
          style={{ display: "none" }}
        >
          Error
        </p>
        <h1>Search For Your Desired Hotel</h1>
      </div>
      <div className="search">
        <div className="row">
          <div className="col-lg-6 col-sm-12">
            <div className="custom-input input-group mb-3">
              <span className="input-group-text">
                <LocationCityIcon />
              </span>
              <input
                type="text"
                className="form-control"
                placeholder="City"
                name="city"
                onChange={changeData}
                value={data.city}
              />
            </div>
          </div>
          <div className="col-lg-6 col-sm-12">
            <div className="custom-input input-group mb-3">
              <span className="input-group-text">
                <SortIcon />
              </span>
              <select
                className="form-select form-control"
                name="sortBy"
                onChange={changeData}
                value={data.sortBy}
                aria-label="Select Role"
              >
                <option
                  value=""
                  selected={data.sortBy === "" ? true : false}
                  disabled
                >
                  Sort By?
                </option>
                <option
                  value="price"
                  selected={data.sortBy === "price" ? true : false}
                >
                  Price
                </option>
                <option
                  value="class"
                  selected={data.sortBy === "class" ? true : false}
                >
                  Class
                </option>
                <option
                  value="distance_from_search"
                  selected={
                    data.sortBy === "distance_from_search" ? true : false
                  }
                >
                  Distance From Search
                </option>
                <option
                  value="bayesian_review_score"
                  selected={
                    data.sortBy === "bayesian_review_score" ? true : false
                  }
                >
                  Bayesian Review Score
                </option>
              </select>
            </div>
          </div>
        </div>
        <div className="row">
          <div className="col-lg-6 col-sm-12">
            <div className="custom-input input-group mb-3">
              <span className="input-group-text">
                <PriceChangeIcon />
              </span>
              <input
                type="number"
                className="form-control"
                placeholder="Min Price"
                name="minPrice"
                onChange={changeData}
                value={data.minPrice}
              />
            </div>
          </div>
          <div className="col-lg-6 col-sm-12">
            <div className="custom-input input-group mb-3">
              <span className="input-group-text">
                <PriceChangeIcon />
              </span>
              <input
                type="number"
                className="form-control"
                placeholder="Max Price"
                name="maxPrice"
                onChange={changeData}
                value={data.maxPrice}
              />
            </div>
          </div>
        </div>
        <div className="row">
          <div className="col-lg-3 col-sm-12">
            <div className="custom-input input-group mb-3">
              <span className="input-group-text">
                <BedIcon />
              </span>
              <input
                type="number"
                className="form-control"
                placeholder="No. of Rooms"
                name="rooms"
                onChange={changeData}
                value={data.rooms}
              />
            </div>
          </div>
          <div className="col-lg-3 col-sm-12">
            <div className="custom-input input-group mb-3">
              <span className="input-group-text">
                <PersonIcon />
              </span>
              <input
                type="number"
                className="form-control"
                placeholder="No. of Adults"
                name="adults"
                onChange={changeData}
                value={data.adults}
              />
            </div>
          </div>
          <div className="col-lg-3 col-sm-12">
            <div className="custom-input input-group mb-3">
              <span className="input-group-text">
                <PersonIcon />
              </span>
              <input
                type="number"
                className="form-control"
                placeholder="No. of Children"
                name="children"
                onChange={changeData}
                value={data.children}
              />
            </div>
          </div>

          <div className="col-lg-3 col-sm-12">
            <div className="custom-input input-group mb-3">
              <span className="input-group-text">
                <LayersIcon />
              </span>
              <input
                type="number"
                className="form-control"
                placeholder="Max Pages"
                name="maxPages"
                onChange={changeData}
                value={data.maxPages}
              />
            </div>
          </div>
        </div>
        <div className="row">
          <div className="col-lg-6 col-sm-12">
            <label>Start Date*</label>
            <div className="custom-input input-group mb-3">
              <span className="input-group-text">
                <DateRangeIcon />
              </span>
              <input
                type="date"
                className="form-control"
                placeholder="Start Date"
                name="start_datetime"
                onChange={changeData}
                value={data.start_datetime}
              />
            </div>
          </div>
          <div className="col-lg-6 col-sm-12">
            <label>End Date*</label>
            <div className="custom-input input-group mb-3">
              <span className="input-group-text">
                <DateRangeIcon />
              </span>
              <input
                type="date"
                className="form-control"
                placeholder="End Date"
                name="end_datetime"
                onChange={changeData}
                value={data.end_datetime}
              />
            </div>
          </div>
        </div>
        <div className="w-100 mt-1 custom-button">
          <button
            type="button"
            className="btn btn-primary"
            style={{
              padding: "12px 15px",
            }}
            onClick={CONSTANT.test ? test : applyFilters}
          >
            Apply Filters
          </button>
        </div>
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
                      {hotel.price && hotel.currency ? (
                        <span className="custom-card-address mb-1">
                          <span className="text-muted">Price : </span>
                          <span className="c-bold">
                            {hotel.price}
                            {hotel.currency}
                          </span>
                        </span>
                      ) : null}
                      {hotel.rating ? (
                        <span className="custom-card-address mt-4 mb-1">
                          <span className="text-muted">Ratings : </span>
                          <span className="c-bold">{hotel.rating}</span>
                        </span>
                      ) : null}
                      {hotel.reviews ? (
                        <span className="custom-card-address mb-1">
                          <span className="text-muted">Reviews : </span>
                          <span className="c-bold">{hotel.reviews}</span>
                        </span>
                      ) : null}
                      {hotel.stars ? (
                        <span className="custom-card-address mb-1">
                          <span className="text-muted">Stars : </span>
                          <span className="c-bold">{hotel.stars}</span>
                        </span>
                      ) : null}

                      {hotel.url ? (
                        <span className="custom-card-address mb-1">
                          <span className="text-muted">Details : </span>
                          <a className="c-bold" href={hotel.url}>
                            Visit
                          </a>
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
                            makeReservation(e, index);
                          }}
                        >
                          Make Reservation
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
        ""
      )}
    </div>
  );
}
