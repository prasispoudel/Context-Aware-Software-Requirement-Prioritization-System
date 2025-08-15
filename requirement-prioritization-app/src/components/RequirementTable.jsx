//import React, { useContext } from 'react';
//import { AppContext } from '../App';

const RequirementTable = ({ requirements, onSelect }) => (
  <div className="overflow-x-auto rounded-lg shadow">
    <table className="min-w-full border-collapse border border-gray-200 bg-white rounded-lg">
      <thead>
        <tr>
          <th className="border px-4 py-2 bg-gray-100 text-left">ID</th>
          <th className="border px-4 py-2 bg-gray-100 text-left">Statement</th>
          <th className="border px-4 py-2 bg-gray-100 text-left">Features</th>
          {onSelect && <th className="border px-4 py-2 bg-gray-100 text-left">Select</th>}
        </tr>
      </thead>
      <tbody>
        {requirements.map((req) => (
          <tr key={req.id} className="hover:bg-blue-50 transition">
            <td className="border px-4 py-2">{req.id}</td>
            <td className="border px-4 py-2">{req.text}</td>
            <td className="border px-4 py-2">
              {/* Show priorityScore if available */}
              {req.priorityScore !== undefined && (
                <span className="mr-2 font-bold text-blue-700">Priority Score: {req.priorityScore}</span>
              )}
              {req.contextualFeatures &&
                Object.entries(req.contextualFeatures).map(([k, v]) => (
                  <span key={k} className="mr-2 bg-gray-100 px-2 py-1 rounded text-xs">{k}: {v}</span>
                ))}
            </td>
            {onSelect && (
              <td className="border px-4 py-2">
                <button
                  className="bg-blue-500 hover:bg-blue-600 text-white px-3 py-1 rounded shadow transition"
                  onClick={() => onSelect(req)}
                >
                  Select
                </button>
              </td>
            )}
          </tr>
        ))}
      </tbody>
    </table>
  </div>
);

window.RequirementTable = RequirementTable;