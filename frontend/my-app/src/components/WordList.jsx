export default function WordList({ words, onSelect, onDelete }) {
  const speak = (text) => {
    const utterance = new SpeechSynthesisUtterance(text)
    utterance.lang = 'en-US'
    window.speechSynthesis.speak(utterance)
  }

  return (
    <section className="p-6 max-w-6xl mx-auto">
      <h3 className="text-4xl font-extrabold mb-8 text-indigo-900 tracking-wide">
        Words to Learn Today
      </h3>

      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-8">
        {words.map((wordObj) => {
          const { word, vietnamese, pronunciation, imageUrl, example, synonym } = wordObj
          const exampleList = Array.isArray(example) ? example : [example]
          const synonymText = Array.isArray(synonym) ? synonym.join('; ') : synonym

          return (
            <div
              key={wordObj.word_id}
              className="group bg-white rounded-xl shadow-md p-6 flex flex-col items-center text-indigo-900 font-semibold text-lg relative"
            >
              {imageUrl && (
                <img
                  src={imageUrl}
                  alt={word}
                  className="w-24 h-24 object-cover rounded-full mb-4 border-4 border-indigo-200 group-hover:border-indigo-400 transition-colors"
                />
              )}

              <div
                onClick={() =>
                  onSelect &&
                  onSelect({
                    word,
                    vietnamese,
                    pronunciation,
                    imageUrl,
                    example: exampleList.join('\n'),
                    synonym: synonymText,
                  })
                }
                className="cursor-pointer text-center"
              >
                <div className="flex justify-center items-center space-x-2 mb-1">
                  <span className="text-2xl">{word}</span>
                  <button
                    onClick={(e) => {
                      e.stopPropagation()
                      speak(word)
                    }}
                    className="text-indigo-600 hover:text-indigo-800"
                    aria-label={`Phát âm từ ${word}`}
                    title={`Nghe phát âm "${word}"`}
                  >
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      className="h-5 w-5"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                      strokeWidth={2}
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        d="M11 5L6 9H2v6h4l5 4V5zM15.54 8.46a5 5 0 010 7.07M19.07 4.93a10 10 0 010 14.14"
                      />
                    </svg>
                  </button>
                </div>

                {pronunciation && (
                  <span className="text-gray-500 italic text-sm block mb-1">
                    {pronunciation}
                  </span>
                )}

                <small className="text-indigo-600 italic text-sm tracking-wide">
                  {vietnamese}
                </small>
              </div>

              {onDelete && (
                <button
                  onClick={() => onDelete(wordObj)}
                  aria-label={`Delete ${word}`}
                  title={`Delete ${word}`}
                  className="absolute top-2 right-2 text-red-600 hover:text-red-800 transition"
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    className="h-6 w-6"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                    strokeWidth={2}
                  >
                    <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              )}
            </div>
          )
        })}
      </div>
    </section>
  )
}
