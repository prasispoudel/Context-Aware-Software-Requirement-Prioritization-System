// No import/export statements! Use only global variables.

const ContextualFeatureDropdowns = ({ onChange, values }) => (
  <div className="grid grid-cols-2 gap-4 mb-4 w-full max-w-lg mx-auto bg-white p-6 rounded-lg shadow">
    {Object.keys(values).map((feature) => (
      <div key={feature}>
        <label className="block font-semibold mb-1 capitalize text-gray-700">{feature}</label>
        <select
          className="border p-2 w-full rounded focus:ring-blue-500 focus:border-blue-500"
          value={values[feature]}
          onChange={(e) => onChange(feature, Number(e.target.value))}
        >
          <option value={1}>Very Low</option>
          <option value={2}>Low</option>
          <option value={3}>Medium</option>
          <option value={4}>High</option>
          <option value={5}>Very High</option>
        </select>
      </div>
    ))}
  </div>
);

// Register globally for UMD usage
window.ContextualFeatureDropdowns = ContextualFeatureDropdowns;
