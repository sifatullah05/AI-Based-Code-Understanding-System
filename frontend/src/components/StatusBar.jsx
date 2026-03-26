import { useEffect, useState } from "react";
import { getStatus } from "../api/api";

export default function StatusBar() {
  const [status, setStatus] = useState({ indexing: false, repo_id: null });

  useEffect(() => {
    const interval = setInterval(async () => {
      const res = await getStatus();
      setStatus(res);
    }, 3000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="p-2 mb-4 bg-gray-100 dark:bg-gray-700 rounded text-sm text-gray-900 dark:text-gray-100 w-full max-w-2xl">
      {status.indexing
        ? `Indexing in progress: ${status.repo_id}`
        : "No indexing in progress"}
    </div>
  );
}