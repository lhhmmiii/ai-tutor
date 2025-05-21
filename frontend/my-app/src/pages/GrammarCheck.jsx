import { useState, useEffect } from 'react'
import TextAreaWithButton from '../components/TextAreaWithButton'
import ErrorList from '../components/ErrorList'
import Chatbot from '../components/Chatbot'
import { grammar_check } from '../services/writing_service'

function GrammarCheck() {
  const [text, setText] = useState('')
  const [result, setResult] = useState([])
  const [correctedText, setCorrectedText] = useState('')
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    console.log('Updated result:', result)
  }, [result])

  const handleGrammarCheck = async () => {
    if (!text.trim()) return

    setLoading(true)
    try {
      const user_id = localStorage.getItem('user_id')
      const data = await grammar_check(user_id, text)

      const issues = Array.isArray(data.issues_found)
        ? data.issues_found.map(issue => ({
            original: issue.original,
            corrected: issue.corrected,
            explanation: issue.explanation,
          }))
        : []

      setCorrectedText(data.corrected_text || '')
      setResult(issues)
    } catch (error) {
      console.error('Error during grammar check:', error.response?.data || error.message)
    } finally {
      setLoading(false)
    }
  }

  const handleFileUpload = async (event) => {
    const file = event.target.files[0]
    if (!file) return

    setLoading(true)
    try {
      const user_id = localStorage.getItem('user_id')
      const fileText = await file.text()
      const data = await grammar_check(user_id, fileText)

      const issues = Array.isArray(data.issues_found)
        ? data.issues_found.map(issue => ({
            original: issue.original,
            corrected: issue.corrected,
            explanation: issue.explanation,
          }))
        : []

      setCorrectedText(data.corrected_text || '')
      setResult(issues)
    } catch (error) {
      console.error('Error during file grammar check:', error.response?.data || error.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="w-full min-h-screen bg-indigo-50 py-10 px-4">
      <Chatbot />

      <h1 className="text-4xl font-extrabold text-blue-900 mb-10 text-center select-none">
        Grammar Check
      </h1>

      <div className="w-full max-w-6xl mx-auto flex flex-col md:flex-row gap-6">
        {/* Input section */}
        <div className="flex-1 relative">
          <TextAreaWithButton text={text} setText={setText} onCheck={handleGrammarCheck} />
          <input
            type="file"
            accept=".txt"
            onChange={handleFileUpload}
            className="mt-4"
          />
          {loading && (
            <div className="flex items-center space-x-2 absolute top-full mt-2 text-blue-600 font-semibold select-none">
              <svg
                className="animate-spin h-5 w-5 text-blue-600"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
              >
                <circle
                  className="opacity-25"
                  cx="12"
                  cy="12"
                  r="10"
                  stroke="currentColor"
                  strokeWidth="4"
                ></circle>
                <path
                  className="opacity-75"
                  fill="currentColor"
                  d="M4 12a8 8 0 018-8v8z"
                ></path>
              </svg>
              <span>Checking grammar, please wait...</span>
            </div>
          )}
        </div>

        {/* Corrected output */}
        {correctedText && (
          <div className="flex-1 bg-white p-6 rounded-lg shadow-lg">
            <h2 className="text-2xl font-bold text-green-700 mb-4">Corrected Text</h2>
            <p className="text-gray-800 whitespace-pre-line">{correctedText}</p>
          </div>
        )}
      </div>

      {/* Error list */}
      <div className="w-full max-w-6xl mx-auto mt-8">
        <ErrorList result={result} />
      </div>
    </div>
  )
}

export default GrammarCheck
