// src/components/WordDetailsModal.jsx

export default function WordDetails({ wordObj, onClose }) {
  if (!wordObj) return null

  return (
    <>
      {/* Overlay */}
      <div
        className="fixed inset-0 bg-black bg-opacity-50 backdrop-blur-sm z-40"
        onClick={onClose}
      ></div>

      {/* Modal */}
      <div className="fixed top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2
        bg-white rounded-xl shadow-2xl max-w-lg w-full p-8 z-50">
        <h2 className="text-2xl font-bold mb-5 text-indigo-900 text-center">
          Details for "{wordObj.word}"
        </h2>
        <table className="w-full border-collapse border border-gray-200">
          <tbody>
            <tr className="bg-indigo-50 border border-gray-200">
              <td className="p-4 font-semibold text-indigo-900 w-48">Vietnamese Meaning</td>
              <td className="p-4">{wordObj.vietnamese}</td>
            </tr>

            <tr className="border border-gray-200 align-top">
              <td className="p-4 font-semibold text-indigo-900">Example Sentences</td>
              <td className="p-4">
                <ul className="list-disc pl-5 space-y-1 text-gray-700 italic">
                  {wordObj.example
                    .split('\n')
                    .filter((ex) => ex.trim())
                    .map((ex, index) => (
                      <li key={index}>"{ex.trim()}"</li>
                    ))}
                </ul>
              </td>
            </tr>

            <tr className="bg-indigo-50 border border-gray-200">
              <td className="p-4 font-semibold text-indigo-900">Synonym</td>
              <td className="p-4">{wordObj.synonym}</td>
            </tr>

            <tr className="border border-gray-200">
              <td className="p-4 font-semibold text-indigo-900">Image</td>
              <td className="p-4 text-center">
                {wordObj.imageUrl ? (
                  <img
                    src={wordObj.imageUrl}
                    alt={wordObj.word}
                    className="mx-auto rounded-lg shadow-md max-h-48 object-cover"
                  />
                ) : (
                  <span className="text-gray-400 italic">No image available</span>
                )}
              </td>
            </tr>
          </tbody>
        </table>

        <button
          onClick={onClose}
          className="mt-6 block mx-auto bg-indigo-600 hover:bg-indigo-700 text-white px-6 py-2 rounded-lg transition"
        >
          Close
        </button>
      </div>
    </>
  )
}
