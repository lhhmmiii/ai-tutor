import { useState } from 'react'
import TextAreaWithButton from '../components/TextAreaWithButton'
import ErrorList from '../components/ErrorList'

function GrammarCheck() {
  const [text, setText] = useState('')
  const [result, setResult] = useState(null)

  const handleGrammarCheck = () => {
    if (!text.trim()) return
    setResult({
      errors: [
        { error: 'Thiếu mạo từ', explanation: 'Bạn quên "a" trước danh từ.' },
        { error: 'Sai thì động từ', explanation: 'Hãy dùng thì quá khứ thay vì hiện tại.' },
      ],
    })
  }

  return (
    <div className="w-full min-h-full">
      <h1 className="text-4xl font-extrabold text-blue-900 mb-10 text-center select-none">
        Grammar Check
      </h1>

      <div className="w-full">
        <TextAreaWithButton text={text} setText={setText} onCheck={handleGrammarCheck} />
        <ErrorList result={result} />
      </div>
    </div>
  )
}

export default GrammarCheck
