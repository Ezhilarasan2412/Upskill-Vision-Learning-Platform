import React, { useState, useEffect } from "react";
import axios from "axios";

const ManageDepartmentParticipants = () => {
  const [departments, setDepartments] = useState([]);
  const [selectedDepartment, setSelectedDepartment] = useState("");
  const [manager, setManager] = useState(null);
  const [allParticipants, setAllParticipants] = useState([]);
  const [departmentParticipants, setDepartmentParticipants] = useState([]);

  useEffect(() => {
    fetchDepartments();
    fetchAllParticipants();
  }, []);

  // Fetch departments
  const fetchDepartments = async () => {
    try {
      const res = await axios.get("http://localhost:5000/api/departments");
      setDepartments(res.data);
    } catch (error) {
      console.error("Error fetching departments:", error);
    }
  };

  // Fetch all participants
  const fetchAllParticipants = async () => {
    try {
      const res = await axios.get("http://localhost:5000/api/participants");
      setAllParticipants(res.data);
    } catch (error) {
      console.error("Error fetching participants:", error);
    }
  };

  // Fetch participants of the selected department
  const fetchDepartmentParticipants = async (departmentId) => {
    try {
      const res = await axios.get(`http://localhost:5000/api/departments/${departmentId}/participants`);
      setDepartmentParticipants(res.data);
      fetchManagerOfDepartment(departmentId);
    } catch (error) {
      console.error("Error fetching department participants:", error);
    }
  };

  // Fetch manager of the selected department
  const fetchManagerOfDepartment = async (departmentId) => {
    try {
      const department = departments.find(dep => dep.department_id === departmentId);
      if (department) {
        const managerRes = await axios.get(`http://localhost:5000/api/users/${department.manager_id}`);
        setManager(managerRes.data);
      }
    } catch (error) {
      console.error("Error fetching department manager:", error);
    }
  };

  // Handle adding participant to the department
  const handleAddParticipant = async (participantId) => {
    if (!selectedDepartment) {
      alert("Please select a department first.");
      return;
    }

    try {
      await axios.post(`http://localhost:5000/api/departments/${selectedDepartment}/participants`, {
        participant_ids: [participantId],
      });
      alert("Participant added successfully!");
      fetchDepartmentParticipants(selectedDepartment); // Refresh the participant list
    } catch (error) {
      console.error("Error adding participant:", error);
      alert("Failed to add participant.");
    }
  };

  // Handle removing participant from the department
  const handleRemoveParticipant = async (participantId) => {
    try {
      await axios.delete(`http://localhost:5000/api/departments/${selectedDepartment}/participants/${participantId}`);
      alert("Participant removed successfully!");
      fetchDepartmentParticipants(selectedDepartment); // Refresh the participant list
    } catch (error) {
      console.error("Error removing participant:", error);
      alert("Failed to remove participant.");
    }
  };

  return (
    <div className="container mx-auto p-4">
      <h3 className="text-xl font-bold mb-4">Manage Department Participants</h3>

      <select
        className="border p-2 w-full mb-2"
        value={selectedDepartment}
        onChange={(e) => {
          setSelectedDepartment(e.target.value);
          fetchDepartmentParticipants(e.target.value);
        }}
      >
        <option value="">Select Department</option>
        {departments.map((department) => (
          <option key={department.department_id} value={department.department_id}>
            {department.department_name}
          </option>
        ))}
      </select>

      {manager && (
        <div>
          <h4>Manager: {manager.first_name} {manager.last_name}</h4>
        </div>
      )}

      <h3 className="text-xl font-bold mb-4">Current Participants</h3>
      <div>
        {departmentParticipants.map((participant) => (
          <div key={participant.user_id} className="flex items-center mb-2">
            <span>{participant.first_name} {participant.last_name}</span>
            <button
              onClick={() => handleRemoveParticipant(participant.user_id)}
              className="bg-red-500 text-white p-2 rounded ml-4"
            >
              Remove
            </button>
          </div>
        ))}
      </div>

      <h3 className="text-xl font-bold mb-4">Available Participants</h3>
      <div>
        {allParticipants.map((participant) => (
          <div key={participant.user_id} className="flex items-center mb-2">
            <span>{participant.first_name} {participant.last_name}</span>
            <button
              onClick={() => handleAddParticipant(participant.user_id)}
              className="bg-green-500 text-white p-2 rounded ml-4"
            >
              Add
            </button>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ManageDepartmentParticipants;
