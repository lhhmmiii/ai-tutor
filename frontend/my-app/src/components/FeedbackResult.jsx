// src/components/FeedbackResult.jsx
export default function FeedbackResult({ feedback }) {
    return (
      <div className="mt-8 p-6 bg-white rounded-lg shadow-md border border-gray-200 max-w-3xl">
        <h3 className="text-xl font-semibold mb-2">Feedback:</h3>
        <p className="text-gray-800 whitespace-pre-line">{feedback}</p>
      </div>
    )
  }
  