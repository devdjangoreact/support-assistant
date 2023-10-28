import React, { useState, ChangeEvent } from "react";

const App: React.FC = () => {
  const [question, setQuestion] = useState<string>("");
  const [answer, setAnswer] = useState<string>("");

  const handleQuestionChange = (event: ChangeEvent<HTMLTextAreaElement>) => {
    setQuestion(event.target.value);
  };

  const handleSubmit = async () => {
    try {
      const response = await fetch(
        (process.env.REACT_APP_API_ENDPOINT + "/ai/get_answer") as string,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ question: question }),
        }
      );
      const data = await response.json();
      setAnswer(data.answer);
    } catch (error) {
      console.error("Error fetching the answer:", error);
    }
  };

  return (
    <div className="h-screen flex items-center justify-center bg-gray-200">
      <div className="bg-white p-6 rounded-lg shadow-lg max-w-xl w-full">
        <h1 className="text-2xl font-bold mb-4">Ask a Question</h1>
        <textarea
          className="p-2 w-full border rounded-md resize-none mb-4"
          rows={4}
          value={question}
          onChange={handleQuestionChange}
          placeholder="Enter your question"
        />
        <button
          className="w-full bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-md transition duration-300 ease-in-out"
          onClick={handleSubmit}
        >
          Get Answer
        </button>
        {answer && (
          <div className="mt-4 p-4 bg-gray-100 rounded-md">
            <h2 className="font-medium text-lg mb-2">Answer:</h2>
            <p>{answer}</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default App;
