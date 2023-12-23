// index.js or App.js (where your main component is rendered)
import React from 'react';
import { createRoot } from 'react-dom/client';
import { Provider } from 'react-redux';
import store from './redux/store/configureStore'; // Import your Redux store
import App from './App'; // Your main application component

const root = document.getElementById('root');

createRoot(root).render(
  <Provider store={store}>
    <App />
  </Provider>
);
