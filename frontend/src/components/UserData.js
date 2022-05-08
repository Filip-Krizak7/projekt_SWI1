import React from "react";

const UserData = React.createContext({
  session: {
    access_token: "",
    personal: {
      username: "",
      full_name: "",
      email: "",
      hashed_pass: "",
      disabled: null,
    },
    isLoggedIn: false,
  },
  setSession: () => {},
});

export default UserData;
