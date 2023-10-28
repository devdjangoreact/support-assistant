import React, { useState, useEffect } from "react";

type SidebarProps = {
  selectedChatRoom: string;
  setSelectedChatRoom: (chatRoom: string) => void;
};

const Sidebar: React.FC<SidebarProps> = ({
  selectedChatRoom,
  setSelectedChatRoom,
}) => {
  const [chatRooms, setChatRooms] = useState<string[]>([]);
  useEffect(() => {
    // Fetch chat rooms from the FastAPI backend on component mount
    fetch(process.env.REACT_APP_API_ENDPOINT + `/ai/chat-rooms`)
      .then((response) => response.json())
      .then((data) => setChatRooms(data))
      .catch((error) => console.error("Error fetching chat rooms:", error));
  }, []);
  return (
    <div className="w-64 bg-white rounded-lg shadow-md overflow-y-auto">
      <div className="p-4 border-b border-gray-200">
        <h2 className="text-lg font-bold">Chat Rooms</h2>
      </div>
      <ul>
        {chatRooms.map((room) => (
          <li
            key={room}
            className={`p-4 ${
              room === selectedChatRoom ? "bg-gray-300" : "hover:bg-gray-100"
            } cursor-pointer`}
            onClick={() => setSelectedChatRoom(room)}
          >
            {room}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Sidebar;
