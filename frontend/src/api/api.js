import axios from "axios";

const BASE_URL = "http://localhost:8000";

export const ingestRepo = async (repo_url) => {
  try {
    const { data } = await axios.post(`${BASE_URL}/ingest`, { repo_url });
    return data;
  } catch (err) {
    throw err.response?.data || { detail: "API error" };
  }
};

export const chatRepo = async (repo_id, question, session_id) => {
  try {
    const { data } = await axios.post(`${BASE_URL}/chat`, { repo_id, question, session_id });
    return data;
  } catch (err) {
    throw err.response?.data || { detail: "API error" };
  }
};

export const getStatus = async () => {
  const { data } = await axios.get(`${BASE_URL}/status`);
  return data;
};