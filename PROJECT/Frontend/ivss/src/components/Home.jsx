import React from 'react';
import { useSelector } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import { FaUserFriends, FaExclamationTriangle, FaObjectGroup, FaCarCrash } from 'react-icons/fa';
import serviceImage from '../assets/1.jpeg';
import securityImage from '../assets/security image.jpg';
import './Stylesheets/Home.css';

const Home = () => {
  const isLoggedIn = useSelector(state => state.auth.loggedIn);
  const navigate = useNavigate(); 

  const handleCardClick = (path) => {
    if (isLoggedIn) {
      navigate(path); 
    } else {
      alert('Please log in or sign up to access this feature.');
      navigate('/login-signup'); 
    }
  };
  
  return (
    <div className="container mt-5 text-center">
   
      <h2>Advanced Surveillance Solutions</h2>
      <p className="mt-3">
        Experience cutting-edge surveillance technologies with us!
      </p>
      <div className="row">
        <div className="col-md-6">
          <h2>Strong Service is Key to Customer's Peace of Mind</h2>
          <p>
            Strong Customer Service – We are a customer centric company. We
            believe in customer service – from the moment we pick up the phone
            to the minute you have a question; once your system is installed.
            Our team is always timely, professional and easy to deal with.
          </p>
          <p>
            We believe in providing an honest and the best possible solution to
            the queries of our clients as per our best knowledge. As we have
            faith that one satisfied customer is a plant which we nourish with
            our dedication and quality service, which in turn becomes a fruitful
            tree with many referrals in return as fruit of our efforts.
          </p>
        </div>
        <div className="col-md-6">
          <img src={serviceImage} alt="Service" className="img-fluid" />
        </div>
      </div>
      <div className="row mt-5">
        <div className="col-md-3">
          <div
            className="card "
            onClick={() => handleCardClick("/object-detection")}
            style={{ cursor: "pointer" }}
          >
            <FaObjectGroup size={64} className="mb-3" />
            <h5 className="card-title">Object Detection</h5>
          </div>
        </div>
        <div className="col-md-3">
          <div
            className="card"
            onClick={() => handleCardClick("/vehicle-detection")}
            style={{ cursor: "pointer" }}
          >
            <FaCarCrash size={64} className="mb-3" />
            <h5 className="card-title">Vehicle Crash Detection</h5>
          </div>
        </div>
        <div className="col-md-3">
          <div
            className="card"
            onClick={() => handleCardClick("/fall-detection")}
            style={{ cursor: "pointer" }}
          >
            <FaExclamationTriangle size={64} className="mb-3" />
            <h5 className="card-title">Fall Detection</h5>
          </div>
        </div>
        <div className="col-md-3">
          <div
            className="card text-center"
            onClick={() => handleCardClick("/social-distancing")}
            style={{ cursor: "pointer" }}
          >
            <FaUserFriends size={64} className="mb-3" />
            <h5 className="card-title">Social Distancing Detection</h5>
          </div>
        </div>
      </div>
      <div className="row mt-5 security-consultation">
        <div className="col-md-6 security-image">
          <img
            src={securityImage}
            alt="Security System Consultation"
            className="img-fluid"
          />
        </div>
        <div className="col-md-6 security-text">
          <div className="consultation-principles">
            <h2>10 Years of Experience</h2>
            <p className="subheading">Security System Consultation</p>
            <p className="description">
              While providing security system consultation, there are many areas
              which need proper attention and detailed observation of pertaining
              issues related to one’s business or home. We work on the following
              three principles:
            </p>
            <div className="d-flex align-items-start">
              <div className="me-3 principle-number">
                <h3>01</h3>
              </div>
              <div>
                <h4>PREVENT</h4>
                <p>
                  We try to step in your shoes. Therefore will recommend and
                  deploy solutions that will shield you from harm, avoiding
                  issue.
                </p>
              </div>
            </div>
            <div className="d-flex align-items-start">
              <div className="me-3 principle-number">
                <h3>02</h3>
              </div>
              <div>
                <h4>PROTECT</h4>
                <p>
                  We will make safe all that is dear to you, your family or your
                  business.
                </p>
              </div>
            </div>
            <div className="d-flex align-items-start">
              <div className="me-3 principle-number">
                <h3>03</h3>
              </div>
              <div>
                <h4>PROGRESS</h4>
                <p>
                  We have secured your priorities, you can move forwards,
                  worry-free.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;
