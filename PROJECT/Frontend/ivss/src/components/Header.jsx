import React, { useState, useRef, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { FaHome, FaRocket, FaEnvelope, FaGithub, FaUser, FaArrowDown } from 'react-icons/fa';
import { useSelector, useDispatch } from 'react-redux';
import { logout } from '../redux/actions/authActions';
import websiteIcon from '../assets/website-icon.jpg';
import './Stylesheets/Header.css';

const Header = () => {
  const loggedIn = useSelector((state) => state.auth.loggedIn);
  const userEmail = useSelector((state) => state.auth.userEmail);
  const dispatch = useDispatch();
  const [dropdownVisible, setDropdownVisible] = useState(false);
  const [logoutMessage, setLogoutMessage] = useState('');

  const dropdownRef = useRef(null);

  const handleLogout = () => {
    dispatch(logout());
    setLogoutMessage('Logged out successfully!');
  };

  const toggleDropdown = () => {
    setDropdownVisible(!dropdownVisible);
  };

  const closeDropdown = (e) => {
    if (dropdownRef.current && !dropdownRef.current.contains(e.target)) {
      setDropdownVisible(false);
    }
  };

  useEffect(() => {
    const timeout = setTimeout(() => {
      setLogoutMessage('');
    }, 3000);

    return () => clearTimeout(timeout);
  }, [logoutMessage]);

  return (
    <header className="bg-dark text-light py-3">
      <nav className="container d-flex justify-content-between align-items-center">
        <div className="left-side">
          <Link to="/">
            <img
              src={websiteIcon}
              alt="Website Icon"
              className="website-icon rounded-circle"
              width="50"
              height="50"
            />
          </Link>
        </div>
        <div className="right-side">
          <ul className="list-unstyled d-flex mb-0">
            <li className="me-3">
              <Link to="/" className="text-light text-decoration-none">
                <FaHome /> Home
              </Link>
            </li>
            <li className="me-3">
              <Link to="/yolo" className="text-light text-decoration-none">
                <FaRocket /> YOLO
              </Link>
            </li>
            <li className="me-3">
              <Link to="/contact" className="text-light text-decoration-none">
                <FaEnvelope /> Contact Us
              </Link>
            </li>
            <li className="me-3">
              <a
                href="https://github.com"
                className="text-light text-decoration-none"
              >
                <FaGithub /> GitHub
              </a>
            </li>
            {loggedIn ? (
              <li className="position-relative" ref={dropdownRef}>
                <button
                  className="text-light text-decoration-none btn p-0 welcome-button"
                  aria-expanded={dropdownVisible}
                  onClick={toggleDropdown}
                >
                  <FaUser /> Welcome {userEmail}
                  <FaArrowDown />
                </button>
                {dropdownVisible && (
                  <ul className="dropdown-menu" aria-labelledby="userDropdown">
                    <li>
                      <Link to="/dashboard">Profile</Link>
                    </li>
                    <li>
                      <Link onClick={handleLogout} to="/">
                        Logout
                      </Link>
                    </li>
                  </ul>
                )}
              </li>
            ) : (
              <li>
                <Link to="/login-signup" className="text-light text-decoration-none">
                  <FaUser /> Login/Signup
                </Link>
              </li>
            )}
            {logoutMessage && (
              <li className="text-light ml-3">{logoutMessage}</li>
            )}
          </ul>
        </div>
      </nav>
    </header>
  );
};

export default Header;
