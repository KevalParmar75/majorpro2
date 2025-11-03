import React, { useState } from "react";
import axios from "axios";

function App() {
  const [text, setText] = useState("");
  const [emotion, setEmotion] = useState(null);

  const handleAnalyze = async () => {
    try {
      const res = await axios.post("http://127.0.0.1:8000/emotion_api/analyze/", { text });
      setEmotion(res.data);
    } catch (err) {
      console.error(err);
      alert("Error analyzing emotion");
    }
  };

  return (
    <div style={{ textAlign: "center", marginTop: "50px" }}>
      <h2>AI Emotion Analyzer 🤖</h2>
      <textarea
        rows="4"
        cols="50"
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Type something to analyze..."
      />
      <br />
      <button onClick={handleAnalyze}>Analyze Emotion</button>

      {emotion && (
        <div style={{ marginTop: "20px" }}>
          <h3>Detected Emotion: {emotion.emotion}</h3>
          <p>Confidence: {emotion.score}</p>
        </div>
      )}
    </div>
  );
}

export default App;
