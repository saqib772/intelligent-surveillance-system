// authReducer.js

import { LOGIN_SUCCESS, LOGOUT } from '../constants/actionTypes';

const initialState = {
  loggedIn: false,
  userEmail: null,
};

const authReducer = (state = initialState, action) => {
    switch (action.type) {
      case LOGIN_SUCCESS:
  return {
    ...state,
    loggedIn: true,
    userEmail: action.payload.userEmail,
  };
      case LOGOUT:
        return {
          ...state,
          loggedIn: false,
          userEmail: null,
        };
      default:
        return state;
    }
  };
  
  export default authReducer;