import React, { useState, useRef, useEffect } from "react";
import { marked } from "marked";
import { v4 as uuidv4 } from "uuid";
import AssistLeg from "./AssistLeg.png";

export default function ChatUI({ topic, onBack }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [isTyping, setIsTyping] = useState(false);

  const [history, setHistory] = useState([]);
  const [currentChatId, setCurrentChatId] = useState(uuidv4());

  const chatRef = useRef(null);

  const theme = {
    bg: "#0d1117",
    text: "#e6edf3",
    bubbleUser: "#2380e6",
    bubbleAssistant: "#21262d",
    border: "#30363d"
  };

  //  MAPA SIMPLE PARA MOSTRAR EL NOMBRE
  const topicNames = {
    constitucion_vs: "Constitución",
    codigo_trabajo_vs: "Código Sustantivo del Trabajo",
    reglamentos_vs: "Reglamentos Universitarios"
  };

  // Scroll automático
  useEffect(() => {
    if (chatRef.current) {
      chatRef.current.scrollTo({
        top: chatRef.current.scrollHeight,
        behavior: "smooth"
      });
    }
  }, [messages, isTyping]);

  // Guardar historial sin reordenar
  useEffect(() => {
    setHistory(prev => {
      return prev.map(h =>
        h.id === currentChatId ? { ...h, topic, messages } : h
      );
    });
  }, [messages]);

  // Resumir nombre del chat
  function getChatTitle(messages) {
    if (!messages || messages.length === 0) return "Nuevo chat";

    const firstUserMsg = messages.find(m => m.role === "user");
    if (!firstUserMsg) return "Nuevo chat";

    const words = firstUserMsg.text.split(" ");
    const short = words.slice(0, 10).join(" ");
    return short + (words.length > 10 ? "…" : "");
  }

  async function sendMessage() {
    if (!input.trim()) return;

    const userMsg = { role: "user", text: input };
    setMessages(prev => [...prev, userMsg]);
    const question = input;
    setInput("");

    setIsTyping(true);

    const response = await fetch("http://127.0.0.1:8000/api/ask/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ topic, question })
    });

    const data = await response.json();
    setIsTyping(false);

    const botMsg = { role: "assistant", text: data.answer };
    setMessages(prev => [...prev, botMsg]);
  }

  function copyText(text) {
    navigator.clipboard.writeText(text);
  }

  function openChat(chat) {
    setCurrentChatId(chat.id);
    setMessages(chat.messages);
  }

  function newChat() {
    const newId = uuidv4();
    const newEntry = {
      id: newId,
      topic,
      messages: []
    };

    setHistory(prev => [newEntry, ...prev]);
    setCurrentChatId(newId);
    setMessages([]);
  }

  return (
    <div style={{ display: "flex", height: "100vh", background: theme.bg, color: theme.text }}>

      {/* MENU LATERAL */}
      <div
        style={{
          width: 260,
          borderRight: `1px solid ${theme.border}`,
          padding: "20px 15px",
          display: "flex",
          flexDirection: "column",
          gap: 20,
          background: "#161b22"
        }}
      >
        <button
          onClick={onBack}
          style={{
            padding: "10px",
            borderRadius: 8,
            background: "#0b93f6",
            color: "white",
            border: "none",
            cursor: "pointer",
            fontWeight: "bold"
          }}
        >
          ⬅ Regresar
        </button>

        <button
          onClick={newChat}
          style={{
            padding: "10px",
            borderRadius: 8,
            background: "#28a745",
            color: "white",
            border: "none",
            cursor: "pointer",
            fontWeight: "bold"
          }}
        >
          + Nuevo chat
        </button>

        <div style={{ fontWeight: "bold", opacity: 0.7 }}>Historial</div>

        {/* HISTORIAL */}
        <div style={{ overflowY: "auto", flex: 1 }}>
          {history.map(chat => (
            <div
              key={chat.id}
              onClick={() => openChat(chat)}
              style={{
                padding: "10px",
                marginBottom: 10,
                borderRadius: 6,
                cursor: "pointer",
                background: "transparent",
                color: theme.text,
                border:
                  chat.id === currentChatId
                    ? "2px solid rgba(0, 153, 255, 0.4)"
                    : `1px solid ${theme.border}`
              }}
            >
              {getChatTitle(chat.messages)}
            </div>
          ))}
        </div>
      </div>

      {/* PANEL PRINCIPAL */}
      <div style={{ flex: 1, display: "flex", flexDirection: "column" }}>

        {/* HEADER */}
        <div
          style={{
            padding: "14px 20px",
            borderBottom: `1px solid ${theme.border}`,
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            fontWeight: "bold"
          }}
        >
          Asistente Normativo · Chat 
          <span style={{ opacity: 0.7 }}>
            · {topicNames[topic] || topic}
          </span>
        </div>

        {/* MENSAJES */}
        <div
          ref={chatRef}
          style={{
            flex: 1,
            overflowY: "auto",
            overflowX: "hidden",
            padding: "30px 10px"
          }}
        >
          {messages.map((msg, i) => (
            <div
              key={i}
              style={{
                width: "100%",
                display: "flex",
                justifyContent: msg.role === "user" ? "flex-end" : "flex-start",
                marginBottom: 25,
                padding: "0 20px",
                maxWidth: "100%",
                overflow: "hidden"
              }}
            >

              {msg.role === "assistant" && (
                <img
                  src={AssistLeg}
                  alt="logo"
                  style={{
                    width: 42,
                    height: 42,
                    marginRight: 10,
                    marginLeft: 10,
                    borderRadius: "50%",
                    objectFit: "contain"
                  }}
                />
              )}

              <div style={{ maxWidth: "65%" }}>
                <div
                  style={{
                    padding: "14px 18px",
                    borderRadius: 12,
                    background: msg.role === "user" ? theme.bubbleUser : theme.bubbleAssistant,
                    color: msg.role === "user" ? "white" : theme.text
                  }}
                >
                  <div dangerouslySetInnerHTML={{ __html: marked(msg.text) }} />
                </div>

                {msg.role === "assistant" && (
                  <button
                    onClick={() => copyText(msg.text)}
                    style={{
                      marginTop: 6,
                      background: "none",
                      border: "none",
                      color: theme.text,
                      opacity: 0.6,
                      cursor: "pointer",
                      fontSize: 13
                    }}
                  >
                    Copiar
                  </button>
                )}
              </div>

              {msg.role === "user" && (
                <div
                  style={{
                    width: 40,
                    height: 40,
                    marginLeft: 10,
                    marginRight: 35,
                    borderRadius: "50%",
                    background: "#6c757d",
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    color: "white",
                    fontWeight: "bold"
                  }}
                >
                  Tú
                </div>
              )}
            </div>
          ))}

          {isTyping && (
            <div style={{ paddingLeft: 30, opacity: 0.8 }}>
              <span style={{ fontStyle: "italic" }}>El asistente está escribiendo…</span>
            </div>
          )}
        </div>

        {/* INPUT */}
        <div
          style={{
            padding: "15px 20px",
            borderTop: `1px solid ${theme.border}`,
            background: theme.bg,
            display: "flex",
            gap: 10
          }}
        >
          <input
            type="text"
            value={input}
            onChange={e => setInput(e.target.value)}
            placeholder="Escribe tu pregunta…"
            style={{
              flex: 1,
              padding: "12px 16px",
              borderRadius: 25,
              border: `1px solid ${theme.border}`,
              background: "#161b22",
              color: theme.text
            }}
          />

          <button
            onClick={sendMessage}
            style={{
              padding: "12px 20px",
              borderRadius: 25,
              background: "#0b93f6",
              color: "white",
              fontWeight: "bold",
              border: "none",
              cursor: "pointer"
            }}
          >
            ➤
          </button>
        </div>
      </div>
    </div>
  );
}
