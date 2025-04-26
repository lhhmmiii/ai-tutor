function ErrorList({ result }) {
    if (!result) {
      return (
        <div className="text-gray-500 italic">
          The results will be displayed here after checking.
        </div>
      )
    }
  
    return (
      <div className="w-full max-w-3xl mt-8 bg-white p-6 rounded-lg shadow-lg">
        <h2 className="text-2xl font-bold text-green-800 mb-4">Detected Errors:</h2>
        <ul className="list-disc pl-6 space-y-4">
          {result.errors.map((err, index) => (
            <li key={index}>
              <span className="font-semibold text-red-600">{err.error}:</span>{' '}
              <span className="text-gray-700">{err.explanation}</span>
            </li>
          ))}
        </ul>
      </div>
    )
  }
  
  export default ErrorList
  