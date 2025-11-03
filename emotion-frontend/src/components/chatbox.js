import React, { useState } from 'react';
import axios from 'axios';

export default function ChatBox() {
  const [text, setText] = useState('');
  const [response, setResponse] = useState('');

  const handleSend = async () => {
    const res = await axios.post('http://127.0.0.1:8000/api/detect/', { text });
    setResponse(res.data.label + " (" + res.data.score.toFixed(2) + ")");
  };

  return (
    <div>
      <textarea value={text} onChange={(e) => setText(e.target.value)} />
      <button onClick={handleSend}>Analyze Emotion</button>
      <p>Detected Emotion: {response}</p>
    </div>
  );
}
