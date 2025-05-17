import { useState, useEffect } from 'react'
import Chatbot from '../components/Chatbot'
import WordList from '../components/WordList'
import WordDetailsModal from '../components/WordDetails'
import Notification from '../components/Notification'
import { CreateVocabulary, GetVocabulary, DeleteVocabulary } from '../services/writing_service'

export default function Vocabulary() {
  const [words, setWords] = useState([])
  const [selectedWord, setSelectedWord] = useState(null)
  const [isAddModalOpen, setIsAddModalOpen] = useState(false)
  const [inputWord, setInputWord] = useState('')
  const [notification, setNotification] = useState(null)
  const [loading, setLoading] = useState(false)
  const [isFetching, setIsFetching] = useState(true)

  useEffect(() => {
    const fetchWords = async () => {
      try {
        const user_id = localStorage.getItem('user_id')
        const fetchedWords = await GetVocabulary(user_id)
        const formattedWords = fetchedWords.map(word => ({
          word_id: word.word_id,
          word: word.vocabulary.word,
          vietnamese: word.vocabulary.meaning_vn,
          example: word.vocabulary.sample_sentences.join('\n'), // Assuming sample_sentence is an array
          synonym: word.vocabulary.synonyms.join(', '),
          imageUrl: '',
        }))
        setWords(formattedWords)
      } catch (error) {
        console.error(error)
        showNotification('error', 'Lấy dữ liệu thất bại.')
      } finally {
        setIsFetching(false)
      }
    }

    fetchWords()
  }, [])

  const showNotification = (type, message) => {
    setNotification({ type, message })
    setTimeout(() => setNotification(null), 3000)
  }

  const addWord = async (wordToAdd) => {
    const user_id = localStorage.getItem('user_id')
    if (!wordToAdd.trim()) {
      showNotification('error', 'Vui lòng nhập từ!')
      return
    }
    if (words.find((w) => w.word === wordToAdd.trim())) {
      showNotification('error', `Từ "${wordToAdd.trim()}" đã tồn tại`)
      return
    }

    setLoading(true)
    try {
      const answer = await CreateVocabulary(user_id, wordToAdd)
      setWords((prev) => [
        ...prev,
        {
          word_id: answer.word_id,
          word: wordToAdd.trim(),
          vietnamese: answer.vocabulary.meaning_vn,
          example: answer.vocabulary.sample_sentences.join('\n'), // Assuming sample_sentence is an array
          synonym: answer.vocabulary.synonyms.join(', '),
          imageUrl: '',
        },
      ])
      showNotification('success', `Đã thêm từ "${wordToAdd.trim()}"`)
      setIsAddModalOpen(false)
      setInputWord('')
    } catch (error) {
      console.error(error)
      showNotification('error', 'Thêm từ thất bại. Vui lòng thử lại.')
    } finally {
      setLoading(false)
    }
  }

  const deleteWord = async (word_id) => {
    if (!window.confirm('Bạn có muốn xóa từ này?')) return
    setLoading(true)
    try {
      await DeleteVocabulary(word_id)
      setWords((prev) => prev.filter(word => word.word_id !== word_id))
      showNotification('success', 'Đã xóa từ')
    } catch (error) {
      console.error('Error deleting word:', error)
      showNotification('error', 'Xóa từ thất bại. Vui lòng thử lại.')
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    addWord(inputWord)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-100 via-indigo-50 to-white relative">
      <Chatbot />

      <main className="max-w-7xl mx-auto py-16 px-6 relative">
        {isFetching ? (
          <div className="text-center text-indigo-500 text-lg font-medium">Đang tải từ vựng...</div>
        ) : (
          <WordList
            words={words}
            onSelect={setSelectedWord}
            onDelete={(word) => deleteWord(word.word_id)}
          />
        )}
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
            <h2 className="text-xl font-semibold mb-4">Nhập từ mới</h2>
            <form onSubmit={handleSubmit} className="space-y-4">
              <input
                type="text"
                name="word"
                value={inputWord}
                onChange={(e) => setInputWord(e.target.value)}
                placeholder="Nhập từ, cụm từ hoặc câu..."
                className="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                autoFocus
              />
              <div className="flex justify-end space-x-3">
                <button
                  type="button"
                  onClick={() => setIsAddModalOpen(false)}
                  className="px-4 py-2 bg-gray-300 rounded hover:bg-gray-400"
                >
                  Đóng
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700 flex items-center"
                  disabled={loading}
                >
                  {loading ? (
                    <svg className="animate-spin h-5 w-5 mr-2 text-white" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z" />
                    </svg>
                  ) : null}
                  {loading ? 'Đang thêm...' : 'Thêm'}
                </button>
              </div>
            </form>
          </div>
        </>
      )}

      {notification && (
        <Notification
          type={notification.type}
          message={notification.message}
          onClose={() => setNotification(null)}
        />
      )}
    </div>
  )
}
