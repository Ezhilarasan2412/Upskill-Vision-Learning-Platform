import React, { useState, useEffect } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

const DepartmentManagement = () => {
  const [managers, setManagers] = useState([]);
  const [departmentName, setDepartmentName] = useState("");
  const [selectedManager, setSelectedManager] = useState("");
  const [participants, setParticipants] = useState([]);
  const [selectedParticipants, setSelectedParticipants] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    fetchManagers();
    fetchParticipants();
  }, []);

  const fetchManagers = async () => {
    try {
      const res = await axios.get("http://localhost:5000/api/users-manager?role=2");
      setManagers(res.data);
    } catch (error) {
      console.error("Error fetching managers:", error);
    }
  };

  const fetchParticipants = async () => {
    try {
      const res = await axios.get("http://localhost:5000/api/users-manager?role=4");
      setParticipants(res.data);
    } catch (error) {
      console.error("Error fetching participants:", error);
    }
  };

  const createDepartment = async () => {
    if (!departmentName || !selectedManager) {
      alert("Please provide a department name and select a manager.");
      return;
    }
    try {
      const res = await axios.post("http://localhost:5000/api/departments", {
        department_name: departmentName,
        manager_id: selectedManager,
      });
      const newDepartmentId = res.data.department_id;
      assignParticipants(newDepartmentId);
    } catch (error) {
      console.error("Error creating department:", error);
      alert("Failed to create department.");
    }
  };

  const handleParticipantSelection = (participantId) => {
    setSelectedParticipants((prevSelected) =>
      prevSelected.includes(participantId)
        ? prevSelected.filter((id) => id !== participantId)
        : [...prevSelected, participantId]
    );
  };

  const assignParticipants = async (departmentId) => {
    if (selectedParticipants.length === 0) {
      alert("Please select participants.");
      return;
    }
    try {
      await axios.post(`http://localhost:5000/api/departments/${departmentId}/participants`, {
        participant_ids: selectedParticipants,
      });
      alert("Department created and participants assigned successfully!");
      navigate("/department-management-page");
    } catch (error) {
      console.error("Error assigning participants:", error);
      alert("Failed to assign participants.");
    }
  };

  return (
    <div className="container mx-auto p-4">
      <h3 className="text-xl font-bold mb-4">Create Department</h3>
      <input
        type="text"
        placeholder="Department Name"
        className="border p-2 w-full mb-2"
        value={departmentName}
        onChange={(e) => setDepartmentName(e.target.value)}
      />
      <select
        className="border p-2 w-full mb-2"
        value={selectedManager}
        onChange={(e) => setSelectedManager(e.target.value)}
      >
        <option value="">Select Manager</option>
        {managers.map((manager) => (
          <option key={manager.user_id} value={manager.user_id}>
            {manager.first_name} {manager.last_name}
          </option>
        ))}
      </select>
      
      <h3 className="text-xl font-bold mb-4">Assign Participants</h3>
      <div>
        {participants.map((participant) => (
          <div key={participant.user_id} className="flex items-center mb-2">
            <input
              type="checkbox"
              value={participant.user_id}
              checked={selectedParticipants.includes(participant.user_id)}
              onChange={() => handleParticipantSelection(participant.user_id)}
              className="mr-2"
            />
            <span>{participant.first_name} {participant.last_name}</span>
          </div>
        ))}
      </div>

      <button onClick={createDepartment} className="bg-blue-500 text-white p-2 rounded">
        Create Department
      </button>
    </div>
  );
};

export default DepartmentManagement;