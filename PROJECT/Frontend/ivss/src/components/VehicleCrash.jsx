import React, { useState } from 'react';
import { Form, Button, Container, Row, Col } from 'react-bootstrap';
import './Stylesheets/ObjectDetection.css'; // Import your custom CSS file
import { Link } from 'react-router-dom'; 
const VehicleCrash = () => {
  const [file, setFile] = useState(null);
  const [videoLink, setVideoLink] = useState('');

  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0];
    setFile(selectedFile);
    setVideoLink(''); // Resetting the video link when a file is selected
  };

  const handleVideoLinkChange = (event) => {
    setVideoLink(event.target.value);
    setFile(null); // Resetting the file when a video link is entered
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    // Add logic to handle file submission and video link here
    if (file) {
      console.log('File uploaded:', file);
      // You can perform further actions with the uploaded file
    } else if (videoLink) {
      console.log('Video link:', videoLink);
      // You can perform actions with the video link
    } else {
      console.log('Please select a file or enter a video link.');
    }
  };

  return (
    <Container className="object-detection-container">
      <Row>
        <Col md={{ span: 6, offset: 3 }} className="object-detection-form">
          <h2>Vehicle Crash Detection</h2>
          <Form onSubmit={handleSubmit}>
            <Form.Group controlId="fileOrVideo">
              <Form.Label>Upload File or Enter Video Link</Form.Label>
              <Form.Control
                type="file"
                accept="video/*"
                onChange={handleFileChange}
                style={{ marginBottom: '10px' }}
              />
              <Form.Control
                type="text"
                placeholder="Enter video link"
                value={videoLink}
                onChange={handleVideoLinkChange}
              />
            </Form.Group>
            <Button variant="primary" type="submit">
              Submit
            </Button>
          </Form>
        </Col>
      </Row>

      <Row className="other-services">
        <Col md={{ span: 6, offset: 3 }}>
          <h3>Other Detection Services</h3>
          <p>Explore additional detection services:</p>
          <ul>
            <li>
              <Link to="/object-detection">
                Object Detection
              </Link>
            </li>
            <li>
              <Link to="/fall-detection">
                Fall Detection
              </Link>
            </li>
            <li>
              <Link to="/social-distancing">
                Social Distancing Detection
              </Link>
            </li>
            {/* Add other service links if needed */}
          </ul>
        </Col>
      </Row>
    </Container>
  );
};

export default VehicleCrash;
