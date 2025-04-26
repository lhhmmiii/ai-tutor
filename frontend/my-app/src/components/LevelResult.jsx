// src/components/LevelResult.jsx
export default function LevelResult({ level }) {
    return (
      <div className="mt-8 p-6 bg-white rounded-lg shadow-md border border-gray-200 max-w-md">
        <h3 className="text-xl font-semibold mb-2">Your writing level is:</h3>
        <p className="text-blue-600 text-3xl font-bold">{level}</p>
      </div>
    )
  }
  