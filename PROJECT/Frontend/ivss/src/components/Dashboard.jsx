import React, { useState } from 'react';
import './Stylesheets/Dashboard.css';
const Dashboard = () => {
  const [user] = useState({
    name: 'John Doe',
    email: 'johndoe@example.com',
  });

  const [lastLogin] = useState('2023-12-15 09:30:00');

  const [servicesUsed] = useState(['Service A', 'Service B', 'Service C']);

  const containerStyle = {
    maxWidth: '800px',
    margin: '0 auto',
    paddingTop: '20px',
  };

  const cardStyle = {
    border: '1px solid #ccc',
    borderRadius: '5px',
    padding: '20px',
    boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)',
  };

  const listGroupItemStyle = {
    backgroundColor: '#f8f9fa',
    borderColor: '#dee2e6',
    color: '#212529',
  };

  return (
    <div style={containerStyle}>
      <h1>User Dashboard</h1>
      <div style={cardStyle}>
        <div>
          <h2>User Information:</h2>
          <p><strong>Name:</strong> {user.name}</p>
          <p><strong>Email:</strong> {user.email}</p>
        </div>
        <div style={{ marginTop: '20px' }}>
          <h2>Activity:</h2>
          <p><strong>Last Logged In:</strong> {lastLogin}</p>
          <h3>Services Used:</h3>
          <ul className="list-group">
            {servicesUsed.map((service, index) => (
              <li key={index} style={listGroupItemStyle} className="list-group-item">{service}</li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
