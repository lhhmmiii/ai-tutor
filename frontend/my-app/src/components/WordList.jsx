export default function WordList({ words, onSelect }) {
  return (
    <section className="p-6 max-w-6xl mx-auto">
      <h3 className="text-4xl font-extrabold mb-8 text-indigo-900 tracking-wide">
        Words to Learn Today
      </h3>

      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-8">
        {words.map(({ word, vietnamese, imageUrl, example, synonym }) => (
          <button
            key={word}
            onClick={() => onSelect({ word, vietnamese, imageUrl, example, synonym })}
            className="group bg-white rounded-xl shadow-md p-6 flex flex-col items-center text-indigo-900 font-semibold text-lg
              hover:scale-105 hover:shadow-2xl transition-transform duration-300 focus:outline-none focus:ring-4 focus:ring-indigo-400"
          >
            {imageUrl && (
              <img
                src={imageUrl}
                alt={word}
                className="w-24 h-24 object-cover rounded-full mb-4 border-4 border-indigo-200 group-hover:border-indigo-400 transition-colors"
              />
            )}

            <span className="text-2xl mb-2">{word}</span>
            <small className="text-indigo-600 italic text-sm tracking-wide">{vietnamese}</small>
          </button>
        ))}
      </div>
    </section>
  )
}
