// configureStore.js

import { configureStore } from '@reduxjs/toolkit';
import authReducer from '../reducers/authReducer';

const rootReducer = {
  auth: authReducer,
};

const store = configureStore({
  reducer: rootReducer,
  // Optionally add middleware, devtools configuration, etc.
});

export default store;
