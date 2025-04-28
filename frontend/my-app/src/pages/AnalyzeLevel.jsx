import { useState } from 'react'
import TextAreaWithButton from '../components/TextAreaWithButton'
import LevelResult from '../components/LevelResult'
import Chatbot from '../components/Chatbot' // added

function AnalyzeLevel() {
  const [text, setText] = useState('')
  const [level, setLevel] = useState(null)

  const handleCheck = () => {
    setLevel('B2 Upper-Intermediate')
  }

  return (
    <div className="relative min-h-screen bg-indigo-50">
      <Chatbot /> {/* added */}

      <div className="max-w-3xl mx-auto p-8 bg-white rounded-lg shadow-lg">
        <h2 className="text-4xl font-extrabold mb-8 text-center text-indigo-700">
          Analyze Your Level
        </h2>

        <TextAreaWithButton
          text={text}
          setText={setText}
          onCheck={handleCheck}
        />

        {level && <LevelResult level={level} />}
      </div>
    </div>
  )
}

export default AnalyzeLevel
