import React, { useState, useEffect } from "react";
import Sidebar from "./components/Sidebar";

function App() {
  const [messages, setMessages] = useState<string[]>([]);
  const [inputValue, setInputValue] = useState<string>("");
  const [selectedChatRoom, setSelectedChatRoom] = useState<string>("General");

  useEffect(() => {
    // Fetch chat messages from the FastAPI backend for the selected chat room whenever it changes
    if (selectedChatRoom) {
      fetch(
        process.env.REACT_APP_API_ENDPOINT +
          `/ai/chat-rooms/${selectedChatRoom}/messages`
      )
        .then((response) => response.json())
        .then((data) => setMessages(data))
        .catch((error) =>
          console.error("Error fetching chat messages:", error)
        );
    }
  }, [selectedChatRoom]);

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setInputValue(event.target.value);
  };

  const handleSend = () => {
    if (inputValue.trim() !== "") {
      fetch(
        process.env.REACT_APP_API_ENDPOINT +
          `/ai/chat-room/${selectedChatRoom}/send-message`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ message: inputValue }),
        }
      )
        .then((response) => response.json())
        .then((data) => {
          console.log(data);
          if (data) {
            setMessages((messages) => [...messages, inputValue, ...data]);
          }
        })
        .catch((error) => console.error("Error sending message:", error));

      setInputValue("");
    }
  };

  return (
    <div className="h-screen flex bg-gray-100 p-6">
      <Sidebar
        selectedChatRoom={selectedChatRoom}
        setSelectedChatRoom={setSelectedChatRoom}
      />

      {/* Chat Area */}
      <div className="flex-1 flex flex-col ml-6 bg-white rounded-lg shadow-md">
        {/* Chat header */}
        <div className="p-4 border-b border-gray-200">
          <h1 className="text-lg font-bold">{selectedChatRoom} Chat</h1>
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
