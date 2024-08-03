import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [formData, setFormData] = useState({
    gender: "",
    age: "",
    height:"",
    weight:"",
    duration:"",
    heartbeat:"",
    bodytemp:""
  });

  const [predictedCalories, setPredictedCalories] = useState(null);
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev, [name]: value
    }));
  }

  const handleSubmit = (e) => {
    e.preventDefault();
    axios.post('http://localhost:5000/predict', formData)
      .then(response => {
        console.log("Data sent successfully");
        console.log("Response:", response.data);
        setPredictedCalories(response.data.predicted_calories);
        setError(null);
        sendCaloriesToNode(response.data.predicted_calories); 
      })
      .catch(error => {
        console.log("Error occurred:", error);
        setError("Failed to fetch predicted calories.");
      });
      
      // Clear form data after submission
      // setFormData({
      //   gender:"",
      //   age: "",
      //   height:"",
      //   weight:"",
      //   duration:"",
      //   heartbeat:"",
      //   bodytemp:""
      // });
  }

  const sendCaloriesToNode = (calories) => {
    axios.post('http://localhost:3001/calories', { predicted_calories: calories })
      .then(response => {
        console.log("Calories sent to Node.js successfully");
      })
      .catch(error => {
        console.error("Error sending calories to Node.js:", error);
      });
  }

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <h1>Calories Expenditure calculator</h1>
        <input type='text' name="gender" value={formData.gender} onChange={handleChange} placeholder='Enter Gender' />
        <input type='text' name="age" value={formData.age} onChange={handleChange} placeholder='Age' />
        <input type='text' name="height" value={formData.height} onChange={handleChange} placeholder='Height in cm' />
        <input type='text' name="weight" value={formData.weight} onChange={handleChange} placeholder='Weight in kg' />
        <input type='text' name="duration" value={formData.duration} onChange={handleChange} placeholder='Duration' />
        <input type='text' name="heartbeat" value={formData.heartbeat} onChange={handleChange} placeholder='Heartbeat' />
        <input type='text' name="bodytemp" value={formData.bodytemp} onChange={handleChange} placeholder='Body-temp' />

        <button type='submit'>Predict</button>
      </form>

      {predictedCalories !== null && (
        <div>
          <h2>Predicted Calories: {predictedCalories}</h2>
        </div>
      )}

      {error && (
        <div>
          <p>Error: {error}</p>
        </div>
      )}
    </div>
  );
}

export default App;
