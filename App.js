import React, { useState } from 'react';
import axios from 'axios';
import { useDropzone } from 'react-dropzone';
import './App.css'; // Import your CSS file for styling

function App() {
  const [prediction, setPrediction] = useState(null);
  const [file, setFile] = useState(null);

  const onDrop = acceptedFiles => {
    setFile(acceptedFiles[0]);
  };

  const { getRootProps, getInputProps } = useDropzone({ onDrop });

  const handleUpload = async () => {
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post('http://localhost:5000/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setPrediction(response.data.prediction);
    } catch (error) {
      console.error('Error uploading file:', error);
    }
  };

  return (
    <div className="app">
      <h1 className="title">NETWORK FAILURE PREDICTION</h1>
      <div className="dropzone" {...getRootProps()}>
        <input {...getInputProps()} />
        <p>Drag 'n' drop an Excel file here, or click to select a file</p>
      </div>
      <button onClick={handleUpload} disabled={!file}>Upload and Predict</button>
      {prediction && <div className="prediction">Prediction: {prediction}Expected failure in about {prediction} minutes</div>}
    </div>
  );
}

export default App;
I