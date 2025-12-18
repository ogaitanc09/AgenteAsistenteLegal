import React, { useState } from "react";
import TopicSelector from "./TopicSelector";
import ChatUI from "./ChatUI";

export default function App() {
  const [topic, setTopic] = useState(null);

  return (
    <div style={{ height: "100vh" }}>
      {topic === null ? (
        <TopicSelector onSelect={setTopic} />
      ) : (
        <ChatUI topic={topic} onBack={() => setTopic(null)} />
      )}
    </div>
  );
}
