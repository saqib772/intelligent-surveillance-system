import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { loginSuccess } from "../redux/actions/authActions";
import { useDispatch } from "react-redux";
import "./Stylesheets/LoginSignup.css";

const LoginSignup = () => {
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [successMessage, setSuccessMessage] = useState("");

  const handleToggle = () => {
    setIsLogin(!isLogin);
    setSuccessMessage("");
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const userData = { email, password };

    if (!isLogin) {
      userData.confirmPassword = confirmPassword;
    }

    const url = isLogin
      ? "http://127.0.0.1:5000/login"
      : "http://127.0.0.1:5000/signup";

    try {
      const response = await axios.post(url, userData, {
        headers: {
          "Content-Type": "application/json",
        },
      });

      if (response.status === 200 || response.status === 201) {
        const result = response.data;
        setSuccessMessage(result.message);
        dispatch(loginSuccess(result.userEmail));

        // Delay before redirection (e.g., 2 seconds)
        setTimeout(() => {
          navigate("/");
        }, 2000); // Change the delay time in milliseconds as needed
      } else {
        console.error("Error:", response.statusText);
      }
    } catch (error) {
      console.error("Error:", error);
    }
  };

  return (
    <div className="container mt-5" id="main">
      {successMessage && (
        <div className="alert alert-success" role="alert">
          {successMessage}
        </div>
      )}
      <div className="row justify-content-center">
        <div className="col-md-6">
          <h2 className="mb-4">{isLogin ? "Login" : "Signup"}</h2>
          <form onSubmit={handleSubmit}>
            <div className="mb-3">
              <label htmlFor="email" className="form-label">
                Email address
              </label>
              <input
                type="email"
                className="form-control"
                id="emailInput" // Added ID for email input
                aria-describedby="emailHelp"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
              <div id="emailHelp" className="form-text">
                We'll never share your email with anyone else.
              </div>
            </div>
            <div className="mb-3">
              <label htmlFor="password" className="form-label">
                Password
              </label>
              <input
                type="password"
                className="form-control"
                id="passwordInput" // Added ID for password input
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>
            {!isLogin && (
              <div className="mb-3">
                <label htmlFor="confirmPassword" className="form-label">
                  Confirm Password
                </label>
                <input
                  type="password"
                  className="form-control"
                  id="confirmPasswordInput" // Added ID for confirm password input
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                />
              </div>
            )}
            <div className="mb-3 form-check">
              <input
                type="checkbox"
                className="form-check-input"
                id="rememberMeCheckbox"
              />
              <label className="form-check-label" htmlFor="rememberMeCheckbox">
                Remember me
              </label>
            </div>
            <button
              type="submit"
              className="btn btn-primary me-2"
              id="submitButton"
            >
              {isLogin ? "Login" : "Signup"}
            </button>
            <button
              type="button"
              className="btn btn-secondary"
              onClick={handleToggle}
              id="toggleButton"
            >
              {isLogin ? "Signup" : "Login"}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default LoginSignup;
