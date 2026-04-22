const DependencyTable = ({ dependencies, onEdit, onRemove }) => (
  <div className="overflow-x-auto rounded-lg shadow">
    <table className="min-w-full border-collapse border border-gray-200 bg-white rounded-lg">
      <thead>
        <tr>
          <th className="border px-4 py-2 bg-gray-100 text-left">Root Requirement</th>
          <th className="border px-4 py-2 bg-gray-100 text-left">Node Requirement</th>
          <th className="border px-4 py-2 bg-gray-100 text-left">Actions</th>
        </tr>
      </thead>
      <tbody>
        {dependencies.map((dependency, index) => (
          <tr key={index} className="hover:bg-blue-50 transition">
            <td className="border px-4 py-2">{dependency.source_text || dependency.sourceId}</td>
            <td className="border px-4 py-2">{dependency.target_text || dependency.targetId}</td>
            <td className="border px-4 py-2">
              <button
                className="bg-red-500 hover:bg-red-600 text-white px-3 py-1 rounded mr-2 shadow transition"
                onClick={() => onRemove && onRemove(index)}
              >
                Remove
              </button>
              <button
                className="bg-yellow-500 hover:bg-yellow-600 text-white px-3 py-1 rounded shadow transition"
                onClick={() => onEdit && onEdit(dependency, index)}
              >
                Edit
              </button>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  </div>
);

// Register globally for UMD
window.DependencyTable = DependencyTable;