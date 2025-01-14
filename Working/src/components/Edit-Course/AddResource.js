import React, { useState } from 'react';
import axios from 'axios';

const AddResource = () => {
  const [courseId, setCourseId] = useState('');
  const [moduleId, setModuleId] = useState('');
  const [resourceTitle, setResourceTitle] = useState('');
  const [resourceType, setResourceType] = useState('link');
  const [resourceContent, setResourceContent] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const [successMessage, setSuccessMessage] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Validate input fields
    if (!courseId || !moduleId || !resourceTitle || !resourceContent) {
      setErrorMessage('Please fill all required fields!');
      return;
    }

    // Additional validation for resourceContent based on resourceType
    if (resourceType === 'link' || resourceType === 'file') {
      if (!resourceContent.startsWith('http://') && !resourceContent.startsWith('https://')) {
        setErrorMessage('Please provide a valid URL (starting with http:// or https://).');
        return;
      }
    }

    const data = {
      course_id: courseId,
      module_id: moduleId,
      resource_title: resourceTitle,
      resource_type: resourceType,
      resource_content: resourceContent,
    };

    try {
      const response = await axios.post('http://127.0.0.1:5000/api/add-resource', data);

      if (response.status === 200) {
        setSuccessMessage('Resource added successfully!');
        setErrorMessage('');
        // Clear the form after successful submission
        setCourseId('');
        setModuleId('');
        setResourceTitle('');
        setResourceType('link');
        setResourceContent('');
      }
    } catch (error) {
      if (error.response) {
        setErrorMessage(error.response.data.message || 'Failed to add resource.');
        setSuccessMessage('');
      } else {
        setErrorMessage('Network error. Please try again later.');
        setSuccessMessage('');
      }
    }
  };

  return (
    <div
      style={{
        padding: '20px',
        background: 'linear-gradient(to right, #ff7e5f, #feb47b)',
        backgroundImage: 'url("https://source.unsplash.com/1920x1080/?education,resources")',
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        color: '#fff',
        minHeight: '100vh',
      }}
    >
      <h2 style={{ textAlign: 'center', color: 'white',marginBottom: '20px' }}>Add a New Resource</h2>

      <div
        style={{
          maxWidth: '500px',
          margin: '0 auto',
          backgroundColor: 'white',  // Change the background color to white
          borderRadius: '8px',
          padding: '20px',
          boxShadow: '0 4px 8px rgba(0, 0, 0, 0.2)',
        }}
      >
        {/* Display Success/Error Messages */}
        {errorMessage && <p style={{ color: 'red' }}>{errorMessage}</p>}
        {successMessage && <p style={{ color: 'green' }}>{successMessage}</p>}

        {/* Form to Add Resource */}
        <form onSubmit={handleSubmit}>
          <div style={{ marginBottom: '10px' }}>
            <label htmlFor="courseId" style={{ display: 'block' }}>Course ID</label>
            <input
              type="number"
              id="courseId"
              value={courseId}
              onChange={(e) => setCourseId(e.target.value)}
              placeholder="Enter course ID"
              required
              style={{
                width: '90%',
                padding: '10px',
                borderRadius: '4px',
                border: '1px solid #ccc',
              }}
            />
          </div>

          <div style={{ marginBottom: '10px' }}>
            <label htmlFor="moduleId" style={{ display: 'block' }}>Module ID</label>
            <input
              type="number"
              id="moduleId"
              value={moduleId}
              onChange={(e) => setModuleId(e.target.value)}
              placeholder="Enter module ID"
              required
              style={{
                width: '90%',
                padding: '10px',
                borderRadius: '4px',
                border: '1px solid #ccc',
              }}
            />
          </div>

          <div style={{ marginBottom: '10px' }}>
            <label htmlFor="resourceTitle" style={{ display: 'block' }}>Resource Title</label>
            <input
              type="text"
              id="resourceTitle"
              value={resourceTitle}
              onChange={(e) => setResourceTitle(e.target.value)}
              placeholder="Enter resource title"
              required
              style={{
                width: '90%',
                padding: '10px',
                borderRadius: '4px',
                border: '1px solid #ccc',
              }}
            />
          </div>

          <div style={{ marginBottom: '10px' }}>
            <label htmlFor="resourceType" style={{ display: 'block' }}>Resource Type</label>
            <select
              id="resourceType"
              value={resourceType}
              onChange={(e) => setResourceType(e.target.value)}
              style={{
                width: '90%',
                padding: '10px',
                borderRadius: '4px',
                border: '1px solid #ccc',
              }}
            >
              <option value="link">Link</option>
              <option value="file">File</option>
              <option value="text">Text</option>
            </select>
          </div>

          <div style={{ marginBottom: '20px' }}>
            <label htmlFor="resourceContent" style={{ display: 'block' }}>Resource Content</label>
            <textarea
              id="resourceContent"
              value={resourceContent}
              onChange={(e) => setResourceContent(e.target.value)}
              placeholder="Enter the URL, file link, or details"
              required
              style={{
                width: '90%',
                padding: '10px',
                borderRadius: '4px',
                border: '1px solid #ccc',
                minHeight: '100px',
              }}
            />
          </div>

          <button
            type="submit"
            style={{
              width: '100%',
              padding: '10px',
              backgroundColor:'#10c932',
              color: '#fff',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer',
            }}
          >
            Add Resource
          </button>
        </form>
      </div>
    </div>
  );
};

export default AddResource;