// No import/export statements! Use only global variables.

const DependencyInput = ({ onAddDependency, selectedDependency, onCancelEdit }) => {
  const { appState } = React.useContext(AppContext);
  const [rootRequirementId, setRootRequirementId] = React.useState('');
  const [nodeRequirementId, setNodeRequirementId] = React.useState('');

  React.useEffect(() => {
    if (selectedDependency) {
      setRootRequirementId(selectedDependency.sourceId || '');
      setNodeRequirementId(selectedDependency.targetId || '');
    } else {
      setRootRequirementId('');
      setNodeRequirementId('');
    }
  }, [selectedDependency]);

  const handleAddOrEdit = () => {
    if (rootRequirementId && nodeRequirementId) {
      onAddDependency({
        sourceId: rootRequirementId,
        targetId: nodeRequirementId,
        dependsOn: true,
        confidence: 1.0
      });
      setRootRequirementId('');
      setNodeRequirementId('');
    } else {
      alert('Please select both root and node requirements.');
    }
  };

  return (
    <div className="flex flex-col space-y-4 w-full max-w-lg mx-auto bg-white p-6 rounded-lg shadow">
      <div>
        <label className="block text-sm font-semibold text-gray-700 mb-1">Root Requirement</label>
        <select
          value={rootRequirementId}
          onChange={(e) => setRootRequirementId(e.target.value)}
          className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 px-3 py-2"
        >
          <option value="">Select Root Requirement</option>
          {appState.requirements.map((req) => (
            <option key={req.id} value={req.id}>{req.text}</option>
          ))}
        </select>
      </div>
      <div>
        <label className="block text-sm font-semibold text-gray-700 mb-1">Node Requirement</label>
        <select
          value={nodeRequirementId}
          onChange={(e) => setNodeRequirementId(e.target.value)}
          className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 px-3 py-2"
        >
          <option value="">Select Node Requirement</option>
          {appState.requirements.map((req) => (
            <option key={req.id} value={req.id}>{req.text}</option>
          ))}
        </select>
      </div>
      <div className="flex space-x-2">
        <button
          onClick={handleAddOrEdit}
          className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded shadow transition w-1/2"
        >
          {selectedDependency ? 'Confirm Edit' : 'Add Dependency'}
        </button>
        {selectedDependency && (
          <button
            onClick={onCancelEdit}
            className="bg-gray-500 hover:bg-gray-600 text-white px-4 py-2 rounded shadow transition w-1/2"
          >
            Cancel
          </button>
        )}
      </div>
    </div>
  );
};

// Register globally for UMD usage
window.DependencyInput = DependencyInput;