import { useState } from "react";
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import IngestForm from "./components/IngestForm";
import StatusBar from "./components/StatusBar";
import ChatBox from "./components/ChatBox";
import ThemeToggle from "./components/ThemeToggle";

export default function App() {
  const [repoId, setRepoId] = useState(null);

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-gray-100 p-4 flex flex-col items-center">
      <ToastContainer position="top-right" autoClose={3000} />
      <h1 className="text-3xl font-bold mb-4">GitHub Source Code Analyzer</h1>
      <ThemeToggle />
      <StatusBar />
      <IngestForm setRepoId={setRepoId} />
      {repoId && (
        <div className="w-full max-w-2xl mt-4">
          <h2 className="text-xl font-semibold mb-2">Chat with Repo</h2>
          <ChatBox repoId={repoId} />
        </div>
      )}
    </div>
  );
}