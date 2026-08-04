import { useState } from "react";
import { sendChatMessage } from "../api";

export default function ChatWidget() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const send = async () => {
    if (!input.trim()) return;
    const userMsg = { role: "user", text: input };
    setMessages((m) => [...m, userMsg]);
    setInput("");
    setLoading(true);
    try {
      const reply = await sendChatMessage(userMsg.text);
      setMessages((m) => [...m, { role: "assistant", text: reply }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card chat-container">
      <div className="card-header">
        <h2 className="card-title">
          <span className="card-title-icon">💬</span>
          AI Market Assistant
        </h2>
      </div>
      <div className="chat-history">
        {messages.length === 0 && (
          <div style={{ textTransform: "none", color: "var(--text-muted)", fontSize: "0.85rem", textAlign: "center", margin: "auto" }}>
            Ask anything about market trends, salaries, or required tech skills!
          </div>
        )}
        {messages.map((m, i) => (
          <div
            key={i}
            className={`chat-bubble ${m.role === "user" ? "chat-bubble-user" : "chat-bubble-assistant"}`}
          >
            <div className="chat-role-label">
              {m.role === "user" ? "You" : "Assistant"}
            </div>
            {m.text}
          </div>
        ))}
        {loading && (
          <div className="chat-loading">
            <span>Thinking...</span>
          </div>
        )}
      </div>
      <div className="chat-input-row">
        <input
          className="input-control"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && send()}
          placeholder="e.g. Which category pays the most?"
          disabled={loading}
        />
        <button className="btn btn-primary" onClick={send} disabled={loading}>
          Send
        </button>
      </div>
    </div>
  );
}
