// src/pages/AnalyzeLevel.jsx
import { useState } from 'react'
import TextAreaWithButton from '../components/TextAreaWithButton'
import LevelResult from '../components/LevelResult'

function AnalyzeLevel() {
  const [text, setText] = useState('')
  const [level, setLevel] = useState(null)

  const handleCheck = () => {
    // Giả lập gọi API phân tích text
    // Ví dụ: dựa vào `text` mà set kết quả level
    setLevel('B2 Upper-Intermediate')
  }

  return (
    <div className="max-w-3xl mx-auto p-8 bg-indigo-50 rounded-lg shadow-lg min-h-screen">
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
  )
}

export default AnalyzeLevel
