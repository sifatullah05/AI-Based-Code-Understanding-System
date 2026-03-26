import { useState, useRef, useEffect } from "react";
import { chatRepo } from "../api/api"; // Backend axios call
import { toast, ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

export default function ChatBox({ repoId }) {
  // States
  const [sessionId] = useState(Date.now().toString()); // Unique session
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [darkMode, setDarkMode] = useState(false);

  const chatEndRef = useRef(null);

  // Auto-scroll whenever messages change
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  // Send message handler
  const handleSend = async () => {
    if (!question.trim()) return;
    const userMsg = { sender: "You", text: question };
    setMessages((prev) => [...prev, userMsg]);
    setQuestion("");

    try {
      const res = await chatRepo(repoId, question, sessionId);
      const botMsg = { sender: "Bot", text: res.answer || "No answer" };
      setMessages((prev) => [...prev, botMsg]);
    } catch {
      toast.error("Failed to get response");
      setMessages((prev) => [...prev, { sender: "Bot", text: "Failed to get response" }]);
    }
  };

  // Clear chat history
  const handleClear = () => {
    setMessages([]);
    setQuestion("");
    toast.info("Chat cleared");
  };

  return (
    <div className={`${darkMode ? "dark" : ""} p-4 w-full max-w-2xl mx-auto`}>
      <ToastContainer position="top-right" autoClose={3000} />
      <div className="flex justify-between items-center mb-2">
        <h2 className="text-lg font-bold text-gray-900 dark:text-gray-100">Chat with Repo</h2>
        <div>
          <button
            onClick={() => setDarkMode((prev) => !prev)}
            className="mr-2 px-3 py-1 bg-gray-300 dark:bg-gray-700 rounded text-sm"
          >
            {darkMode ? "Light Mode" : "Dark Mode"}
          </button>
          <button
            onClick={handleClear}
            className="px-3 py-1 bg-red-500 text-white rounded text-sm"
          >
            Clear
          </button>
        </div>
      </div>

      <div className="flex flex-col bg-white dark:bg-gray-800 rounded shadow-md h-[400px] p-4 overflow-hidden">
        <div className="flex-1 overflow-y-auto mb-2">
          {messages.map((m, i) => (
            <div
              key={i}
              className={`mb-2 p-3 rounded-xl shadow-md max-w-[80%] break-words
                ${m.sender === "You"
                  ? "bg-gradient-to-r from-blue-400 to-blue-200 text-white ml-auto"
                  : "bg-gradient-to-r from-gray-200 to-gray-100 text-gray-900 mr-auto"}`}
            >
              <strong>{m.sender}:</strong> {m.text}
            </div>
          ))}
          <div ref={chatEndRef} />
        </div>

        <div className="flex">
          <input
            className="flex-1 p-2 border rounded-l bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-gray-100"
            placeholder="Ask a question..."
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSend()}
          />
          <button
            className="bg-green-600 hover:bg-green-700 text-white px-4 rounded-r"
            onClick={handleSend}
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
}