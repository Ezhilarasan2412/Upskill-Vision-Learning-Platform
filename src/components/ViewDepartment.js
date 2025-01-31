import axios from 'axios';
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const DepartmentDashboard = () => {
  const [loading, setLoading] = useState(true);
  const [department, setDepartment] = useState('');
  const [manager, setManager] = useState('');  // Store manager's name
  const [users, setUsers] = useState([]);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const userId = localStorage.getItem('user_id'); 
    const roleId = localStorage.getItem('role_id'); 

    if (!userId || !roleId) {
      setError('User is not logged in or role information is missing');
      setLoading(false);
      return;
    }

    const fetchDepartmentData = async () => {
      try {
        const response = await axios.get('http://localhost:5000/api/manager/users', {
          params: {
            user_id: userId,
            role_id: roleId,
          },
        });

        if (response.data) {
          setDepartment(response.data.department);
          setManager(response.data.manager);  // Set manager name
          setUsers(response.data.users || []);
        } else {
          setError('No users found or manager not assigned to any department');
        }
        setLoading(false);
      } catch (error) {
        console.error('Error fetching department data:', error);
        setError('Error fetching data');
        setLoading(false);
      }
    };

    fetchDepartmentData();
  }, []);

  if (loading) {
    return <div>Loading department details...</div>;
  }

  if (error) {
    return <div>{error}</div>;
  }

  return (
    <div style={{ background: 'linear-gradient(to right, #6a11cb, #2575fc)', padding: '20px', minHeight: '100vh', color: '#fff' }}>
      <h2 className="department-dashboard-header" style={{ textAlign: 'center', marginBottom: '20px' }}>
        Department Dashboard
      </h2>

      <div style={{ textAlign: 'center', marginBottom: '20px' }}>
        <h3>Department: {department || 'No Department'}</h3>
        <h4>Manager: {manager || 'No Manager'}</h4>  {/* Display manager name */}
      </div>

      <div style={{ textAlign: 'center', marginBottom: '20px' }}>
        <h4>User List</h4>
        {users.length > 0 ? (
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '20px', justifyContent: 'center' }}>
            {users.map((user) => (
              <div
                key={user.user_id}
                style={{
                  margin: '20px',
                  backgroundColor: 'rgba(255, 255, 255, 0.9)',
                  border: '1px solid #e0e0e0',
                  borderRadius: '8px',
                  boxShadow: '0 2px 8px rgba(0, 0, 0, 0.2)',
                  padding: '20px',
                  width: '300px',
                }}
              >
                <h3 style={{ margin: '0 0 10px 0', color: '#333', fontSize: '20px' }}>{user.username}</h3>
                <p style={{ margin: '10px 0', color: '#666', fontSize: '16px' }}>
                  <strong>{user.first_name} {user.last_name}</strong>
                </p>
                <p style={{ margin: '5px 0', color: '#666', fontSize: '14px' }}>
                  <strong>Email:</strong> {user.email}
                </p>
              </div>
            ))}
          </div>
        ) : (
          <p>No users found in this department.</p>
        )}
      </div>

      <div style={{ textAlign: 'center' }}>
        <button
          style={{
            padding: '10px 20px',
            backgroundColor: '#6a11cb',
            color: '#fff',
            border: 'none',
            borderRadius: '5px',
            cursor: 'pointer',
          }}
          onClick={() => navigate('/manager-dashboard')}
        >
          Back to Manager Dashboard
        </button>
      </div>
    </div>
  );
};

export default DepartmentDashboard;
