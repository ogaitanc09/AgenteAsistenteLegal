import React, { useState } from "react";
import TopicSelector from "./components/TopicSelector";
import Chat from "./components/Chat";

function App() {
  const [topic, setTopic] = useState(null);

  return (
    <div>
      {!topic ? (
        <TopicSelector onSelect={(t) => setTopic(t)} />
      ) : (
        <Chat topic={topic} onBack={() => setTopic(null)} />
      )}
    </div>
  );
}


export default App;
