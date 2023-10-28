// App.tsx
import React, { useState } from "react";

function App() {
  const [messages, setMessages] = useState<string[]>([]); // A mock list of chat messages
  const [inputValue, setInputValue] = useState<string>("");

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setInputValue(event.target.value);
  };

  const handleSend = () => {
    if (inputValue.trim() !== "") {
      setMessages([...messages, inputValue]);
      setInputValue("");
    }
  };

  return (
    <div className="h-screen flex flex-col bg-gray-100 p-6">
      <div className="flex flex-col h-full bg-white rounded-lg shadow-md">
        {/* Chat header */}
        <div className="p-4 border-b border-gray-200">
          <h1 className="text-lg font-bold">New Chat</h1>
        </div>

        {/* Messages list */}
        <div className="flex-1 overflow-y-auto p-4">
          {messages.map((message, index) => (
            <div key={index} className="mb-4 p-2 rounded bg-gray-200">
              {message}
            </div>
          ))}
        </div>

        {/* Input area */}
        <div className="border-t border-gray-200 p-4">
          <div className="flex space-x-4">
            <input
              type="text"
              className="flex-1 p-2 border rounded"
              placeholder="Send a message"
              value={inputValue}
              onChange={handleInputChange}
            />
            <button
              className="bg-blue-500 text-white px-4 py-2 rounded"
              onClick={handleSend}
            >
              Send
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
