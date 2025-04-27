import { useState } from 'react'
import Chatbot from '../components/Chatbot'
import WordList from '../components/WordList'
import WordDetailsModal from '../components/WordDetails'
import { VocabularySupport } from '../services/writing_service'


const initialWords = [
  {
    word: 'love',
    vietnamese: 'Tình yêu',
    example: 'He felt a deep love for his country.',
    synonym: 'affection',
    imageUrl:
      'https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=400&q=80',
  },
  {
    word: 'brave',
    vietnamese: 'Dũng cảm',
    example: 'She was brave enough to speak up.',
    synonym: 'courageous',
    imageUrl:
      'https://images.unsplash.com/photo-1500534623283-312aade485b7?auto=format&fit=crop&w=400&q=80',
  },
  {
    word: 'peace',
    vietnamese: 'Hòa bình',
    example: 'We hope for world peace.',
    synonym: 'harmony',
    imageUrl:
      'https://images.unsplash.com/photo-1468071174046-657d9d351a40?auto=format&fit=crop&w=400&q=80',
  },
]

export default function Vocabulary() {
  const [words, setWords] = useState(initialWords)
  const [selectedWord, setSelectedWord] = useState(null)
  const [isAddModalOpen, setIsAddModalOpen] = useState(false)
  const [inputWord, setInputWord] = useState('')

  const addWord = async  (wordToAdd) => {
    if (!wordToAdd.trim()) {
      alert('Please enter a word!')
      return
    }
    if (words.find((w) => w.word === wordToAdd.trim())) {
      alert(`Từ "${wordToAdd.trim()}" is existed`)
      return
    }

    const answer = await VocabularySupport(wordToAdd)
    console.log(answer)

    setWords((prev) => [
      ...prev,
      {
        word: wordToAdd.trim(),
        vietnamese: answer.meaning_vn,
        example: answer.sample_sentence,
        synonym: answer.synonyms,
        imageUrl: '',
      },
    ])
    alert(`Đã thêm từ "${wordToAdd.trim()}"`)
    setIsAddModalOpen(false)
    setInputWord('')
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    addWord(inputWord)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-100 via-indigo-50 to-white relative">
      <Chatbot />

      <main className="max-w-7xl mx-auto py-16 px-6">
        <WordList words={words} onSelect={setSelectedWord} />

        <WordDetailsModal wordObj={selectedWord} onClose={() => setSelectedWord(null)} />
      </main>

      <button
        onClick={() => setIsAddModalOpen(true)}
        className="fixed bottom-8 left-[calc(16rem+4rem)] flex items-center space-x-2 bg-green-600 hover:bg-green-700 text-white px-4 py-3 rounded-full shadow-lg transition"
        aria-label="Open add vocabulary modal"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          className="h-6 w-6"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
          strokeWidth={2}
          aria-hidden="true"
        >
          <path strokeLinecap="round" strokeLinejoin="round" d="M12 4v16m8-8H4" />
        </svg>
        <span>Add Vocabulary</span>
      </button>

      {isAddModalOpen && (
        <>
          <div
            className="fixed inset-0 bg-black bg-opacity-50 backdrop-blur-sm"
            onClick={() => setIsAddModalOpen(false)}
          ></div>

          <div className="fixed top-1/2 left-1/2 max-w-sm w-full p-6 bg-white rounded-lg shadow-lg -translate-x-1/2 -translate-y-1/2 z-50">
            <h2 className="text-xl font-semibold mb-4">Input</h2>
            <form onSubmit={handleSubmit} className="space-y-4">
              <input
                type="text"
                name="word"
                value={inputWord}
                onChange={(e) => setInputWord(e.target.value)}
                placeholder="Nhập từ, cụm từ hoặc câu liên quan tới chúng."
                className="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                autoFocus
              />
              <div className="flex justify-end space-x-3">
                <button
                  type="button"
                  onClick={() => setIsAddModalOpen(false)}
                  className="px-4 py-2 bg-gray-300 rounded hover:bg-gray-400"
                >
                  Close
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700"
                >
                  Add
                </button>
              </div>
            </form>
          </div>
        </>
      )}
    </div>
  )
}
