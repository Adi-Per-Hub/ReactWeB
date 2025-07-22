import React from "react";
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';

function App() {
  const [file, setFile] = React.useState(null);
  const [downloadUrl, setDownloadUrl] = React.useState(null);
  const [loading, setLoading] = React.useState(false);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) return alert("Please select a file to upload.");

    const formdata = new FormData();
    formdata.append("file", file);
    formdata.append("name", file.name.split(".")[0]);

    setLoading(true);
    try {
      const response = await fetch("http://localhost:8000/process/", {
        method: "POST",
        body: formdata,
      });

      const data = await response.json();
      setDownloadUrl(`http://localhost:8000${data.download_url}`);
    } catch (error) {
      alert("Error uploading file. Please try again.");
      console.error("Error uploading file:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App container mt-5">
      <h1 className="mb-4">Welcome to React File Processor</h1>
      <p>This is a simple React application.</p>

      <div className="input-group mb-3 p-3 mb-2 bg-primary-subtle text-primary-emphasis">
        <input
          type="file"
          className="form-control"
          id="inputGroupFile02"
          onChange={handleFileChange}
        />
        
      </div>

      <button className="btn btn-primary mb-3" onClick={handleUpload} disabled={loading}>
        {loading ? "Processing..." : "Upload and Process"}
      </button>

      {downloadUrl && (
        <div className="alert alert-success">
          <p>File processed successfully!</p>
          <a className="btn btn-success" href={downloadUrl} download>
            Download Result
          </a>
        </div>
      )}
    </div>
  );
}

export default App;
