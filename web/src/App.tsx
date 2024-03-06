import axios from 'axios';
import { useState } from 'react';

const App = () => {
  const [message, setMessage] = useState('');
  const [logMessages, setLogMessages] = useState([]);
  const [url, setUrl] = useState('');

  const fetchData = async () => {
    try {
      const formData = new FormData();
      formData.append('url', url);

      const response = await axios.post('/api/download_images', formData);

      setMessage(response.data.message);
      setLogMessages(response.data.log_messages);
    } catch (error) {
      console.error(`Error: ${error}`);
    }
  };

  return (
    <div>
      <input type="text" value={url} onChange={(e) => setUrl(e.target.value)} placeholder="Image URL" />
      <button onClick={fetchData}>Download Images</button>
      <h1>{message}</h1>
      {logMessages.map((logMessage, index) => (
        <p key={index}>{logMessage}</p>
      ))}
    </div>
  );
};

export default App;
