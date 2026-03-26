import { useState } from "react";
import { ingestRepo } from "../api/api";
import { toast } from "react-toastify";

export default function IngestForm({ setRepoId }) {
  const [repoUrl, setRepoUrl] = useState("");
  const [loading, setLoading] = useState(false);

  const handleIngest = async () => {
    if (!repoUrl) return;
    setLoading(true);
    try {
      const res = await ingestRepo(repoUrl);
      if (res.repo_id) {
        setRepoId(res.repo_id);
        toast.success("Repository ingested successfully!");
      } else {
        toast.error(res.detail || "Error ingesting repo");
      }
    } catch {
      toast.error("Failed to ingest repository");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-4 bg-white dark:bg-gray-800 rounded shadow mb-4 w-full max-w-2xl">
      <h2 className="text-xl font-semibold mb-2 text-gray-900 dark:text-gray-100">Ingest GitHub Repo</h2>
      <input
        type="text"
        placeholder="Enter GitHub repo URL"
        className="w-full p-2 border rounded mb-2 bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-gray-100"
        value={repoUrl}
        onChange={(e) => setRepoUrl(e.target.value)}
      />
      <button
        className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded disabled:opacity-50"
        onClick={handleIngest}
        disabled={loading}
      >
        {loading ? "Ingesting..." : "Ingest"}
      </button>
    </div>
  );
}