// src/pages/Vocabulary.jsx
import { useState } from 'react'
import Chatbot from '../components/Chatbot'
import WordList from '../components/WordList'
import WordDetailsModal from '../components/WordDetails'

const wordsToLearn = [
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
  const [selectedWord, setSelectedWord] = useState(null)

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-100 via-indigo-50 to-white">
      <Chatbot />

      <main className="max-w-7xl mx-auto py-16 px-6">
        <WordList words={wordsToLearn} onSelect={setSelectedWord} />

        <WordDetailsModal
          wordObj={selectedWord}
          onClose={() => setSelectedWord(null)}
        />
      </main>
    </div>
  )
}
