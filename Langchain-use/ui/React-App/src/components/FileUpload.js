import React, { useRef } from 'react';
import { FiUpload } from 'react-icons/fi';
import './FileUpload.css';

function FileUpload({ onFileUpload, loading }) {
  const fileInputRef = useRef(null);

  const handleDragOver = (e) => {
    e.preventDefault();
    e.stopPropagation();
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (!loading) {
      const files = e.dataTransfer.files;
      if (files.length > 0) {
        onFileUpload(files[0]);
      }
    }
  };

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      onFileUpload(e.target.files[0]);
    }
  };

  return (
    <div
      className="file-upload"
      onDragOver={handleDragOver}
      onDrop={handleDrop}
      onClick={() => fileInputRef.current?.click()}
    >
      <div className={`upload-content ${loading ? 'loading' : ''}`}>
        <FiUpload size={32} className="upload-icon" />
        <p className="upload-title">
          {loading ? '📤 Uploading...' : '📄 Upload Document'}
        </p>
        <p className="upload-subtitle">
          {loading ? 'Processing your file...' : 'Drag & drop PDF or CSV here'}
        </p>
      </div>
      <input
        ref={fileInputRef}
        type="file"
        accept=".pdf,.csv"
        onChange={handleFileChange}
        style={{ display: 'none' }}
        disabled={loading}
      />
    </div>
  );
}

export default FileUpload;
