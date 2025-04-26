function TextAreaWithButton({ text, setText, onCheck }) {
  return (
    <div className="w-full mb-10">
      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Type or paste your text here..."
        className="w-full min-h-[200px] p-4 border-2 border-blue-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400 resize-none shadow-sm bg-white text-gray-700"
      />

      <button
        onClick={onCheck}
        className="mt-4 w-full bg-blue-600 text-white py-3 rounded-lg font-semibold text-lg hover:bg-blue-700 active:scale-95 transition-all"
      >
        Submit
      </button>
    </div>
  )
}

export default TextAreaWithButton
