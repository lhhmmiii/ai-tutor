import { useState } from 'react'
import TextAreaWithButton from '../components/TextAreaWithButton'
import FeedbackResult from '../components/FeedbackResult'
import Chatbot from '../components/Chatbot' // <<< Thêm nè

function WritingFeedback() {
  const [text, setText] = useState('')
  const [feedback, setFeedback] = useState(null)

  const handleFeedback = () => {
    // Kết nối backend ở đây
    setFeedback('Your writing is clear, but work on varying your sentence structures.')
  }

  return (
    <div className="max-w-3xl mx-auto p-8 bg-indigo-50 rounded-lg shadow-lg min-h-screen relative">
      <Chatbot /> {/* Thêm Chatbot */}

      <h2 className="text-4xl font-extrabold mb-8 text-center text-indigo-700">
        Writing Feedback
      </h2>

      <TextAreaWithButton
        text={text}
        setText={setText}
        onCheck={handleFeedback}
      />

      {feedback && <FeedbackResult feedback={feedback} />}
    </div>
  )
}

export default WritingFeedback
