import React, { useState } from "react";

function App() {
  const [file, setFile] = useState(null);
  const [uploadStatus, setUploadStatus] = useState("");

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setUploadStatus("");
  };

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!file) {
      setUploadStatus("Please select a file first.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("http://localhost:5000/upload-csv", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();
      if (response.ok) {
        setUploadStatus(`Success: ${data.message}`);
      } else {
        setUploadStatus(`Error: ${data.error}`);
      }
    } catch (error) {
      setUploadStatus("Error uploading file.");
    }
  };

  return (
    <div style={{ padding: 40 }}>
      <h2>Upload CSV File</h2>
      <form onSubmit={handleUpload}>
        <input
          type="file"
          accept=".csv"
          onChange={handleFileChange}
        />
        <button type="submit" style={{ marginLeft: 10 }}>
          Upload
        </button>
      </form>
      {uploadStatus && <p>{uploadStatus}</p>}
    </div>
  );
}

export default App;