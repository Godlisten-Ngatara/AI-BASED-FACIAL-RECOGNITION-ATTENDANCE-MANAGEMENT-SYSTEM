// src/hooks/usePost.js
import { useState } from "react";
import axios from "axios";

const usePost = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [data, setData] = useState(null);

  const postData = async (url, payload) => {
    setLoading(true);
    setError(null);
    try {
      const res = await axios.post(url, payload);
      setData(res.data);
      return res.data;
    } catch (err) {
      const message = err.response?.data?.detail?.message || "Something went wrong";
      setError(message);
    } finally {
      setLoading(false);
    }
  };

  return { postData, loading, error, data };
};

export default usePost;
