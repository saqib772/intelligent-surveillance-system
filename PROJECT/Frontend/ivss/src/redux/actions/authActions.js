// authActions.js

import { LOGIN_SUCCESS, LOGOUT } from '../constants/actionTypes';

export const loginSuccess = (userEmail) => ({
    type: LOGIN_SUCCESS,
    payload: { userEmail }, // Ensure the payload structure is an object with userEmail
  });

export const logout = () => ({
  type: LOGOUT,
});
