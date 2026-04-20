import { useState, useEffect } from "react";
import {
  Bot,
  Send,
  Power,
  Clock,
  MessageSquare,
  Sparkles,
  RotateCcw,
  ChevronDown,
  User,
  Settings2,
  Info,
} from "lucide-react";
import { api, ApiError, type ChatResponse } from "../lib/api";

const tones = [
  {
    id: "profesional",
    label: "Profesional",
    desc: "Formal y directo, ideal para negocios B2B",
    emoji: "💼",
  },
  {
    id: "amigable",
    label: "Amigable",
    desc: "Cálido y cercano, perfecto para retail",
    emoji: "😊",
  },
  {
    id: "casual",
    label: "Casual",
    desc: "Relajado y conversacional, para públicos jóvenes",
    emoji: "😎",
  },
];

const scheduleSlots = [
  { day: "Lunes - Viernes", from: "09:00", to: "18:00", active: true },
  { day: "Sábado", from: "10:00", to: "15:00", active: true },
  { day: "Domingo", from: "00:00", to: "00:00", active: false },
];

type Message = {
  role: "user" | "agent";
  text: string;
  time: string;
};

const initialMessages: Message[] = [
  {
    role: "agent",
    text: "¡Hola! 👋 Soy el asistente virtual de Mi Moda Online. ¿En qué puedo ayudarte hoy?",
    time: "10:00",
  },
];

export function AgentePage() {
  const STORAGE_KEY = "agent_chat_messages";

  // Función para convertir markdown simple a HTML
  const processMarkdown = (text: string) => {
    // Convierte **texto** a <b>texto</b>
    return text.replace(/\*\*(.*?)\*\*/g, "<b>$1</b>");
  };

  // Función para renderizar texto con markdown
  const renderMessageText = (text: string, role: string) => {
    const processed = processMarkdown(text);
    
    // Separa por saltos de línea
    const lines = processed.split("\n");
    
    return lines.map((line, idx) => (
      <div key={idx}>
        <div
          dangerouslySetInnerHTML={{ __html: line }}
          style={{
            fontSize: "13.5px",
            color: role === "agent" ? "#374151" : "#fff",
            lineHeight: 1.6,
            whiteSpace: "pre-wrap",
            wordWrap: "break-word",
          }}
        />
        {idx < lines.length - 1 && <div style={{ height: "4px" }} />}
      </div>
    ));
  };

  // Initialize messages from localStorage or use defaults
  const [messages, setMessages] = useState<Message[]>(() => {
    try {
      const stored = localStorage.getItem(STORAGE_KEY);
      return stored ? JSON.parse(stored) : initialMessages;
    } catch {
      return initialMessages;
    }
  });

  // Persist messages to localStorage whenever they change
  useEffect(() => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(messages));
  }, [messages]);

  const [agentActive, setAgentActive] = useState(true);
  const [selectedTone, setSelectedTone] = useState("amigable");
  const [schedule, setSchedule] = useState(scheduleSlots);
  const [inputText, setInputText] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const [error, setError] = useState("");

  const handleSend = async () => {
    if (!inputText.trim()) return;
    if (!agentActive) return;

    setError("");
    const messageToSend = inputText.trim();

    const now = new Date().toLocaleTimeString("es-MX", { hour: "2-digit", minute: "2-digit" });

    setMessages((prev) => [
      ...prev,
      { role: "user", text: messageToSend, time: now },
    ]);
    setInputText("");
    setIsTyping(true);

    try {
      const response = await api.post<ChatResponse>(
        "/chat/me",
        { 
          message: messageToSend,
          history: messages.map(m => ({ role: m.role, content: m.text }))
        },
        true
      );

      setIsTyping(false);
      setMessages((prev) => [
        ...prev,
        { role: "agent", text: response.agent_response, time: now },
      ]);
    } catch (err) {
      setIsTyping(false);
      const message =
        err instanceof ApiError
          ? err.detail
          : "No fue posible conectar con el backend del agente.";
      setError(message);
      setMessages((prev) => [
        ...prev,
        {
          role: "agent",
          text: "No pude responder porque hay un problema de conexión con el backend. Revisa el estado del servidor e intenta de nuevo.",
          time: now,
        },
      ]);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if ((e.ctrlKey || e.metaKey) && e.key === "Enter") {
      // Ctrl+Enter o Cmd+Enter envía el mensaje
      e.preventDefault();
      handleSend();
    }
    // Enter normal crea una nueva línea (behavior por defecto)
  };

  const toggleSchedule = (index: number) => {
    setSchedule((prev) =>
      prev.map((s, i) => (i === index ? { ...s, active: !s.active } : s))
    );
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-5 h-full">
      {/* Left: Configuration */}
      <div className="space-y-5">
        {/* Agent status */}
        <div
          className="rounded-2xl p-5"
          style={{ background: "#fff", border: "1px solid #f1f5f9", boxShadow: "0 1px 8px rgba(0,0,0,0.04)" }}
        >
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div
                className="rounded-xl flex items-center justify-center"
                style={{
                  width: "44px",
                  height: "44px",
                  background: agentActive ? "rgba(99,102,241,0.1)" : "rgba(148,163,184,0.1)",
                }}
              >
                <Bot size={22} style={{ color: agentActive ? "#6366f1" : "#94a3b8" }} />
              </div>
              <div>
                <h3 style={{ fontSize: "15px", fontWeight: 600, color: "#0f172a" }}>
                  Estado del agente
                </h3>
                <div className="flex items-center gap-2 mt-1">
                  <div
                    className="rounded-full"
                    style={{
                      width: "8px",
                      height: "8px",
                      background: agentActive ? "#10b981" : "#94a3b8",
                    }}
                  />
                  <span style={{ fontSize: "12.5px", color: agentActive ? "#10b981" : "#94a3b8", fontWeight: 500 }}>
                    {agentActive ? "Activo — respondiendo consultas" : "Inactivo"}
                  </span>
                </div>
              </div>
            </div>

            {/* Toggle */}
            <button
              onClick={() => setAgentActive(!agentActive)}
              className="relative rounded-full transition-all duration-300"
              style={{
                width: "52px",
                height: "28px",
                background: agentActive ? "linear-gradient(135deg, #6366f1, #8b5cf6)" : "#e2e8f0",
                border: "none",
                cursor: "pointer",
                flexShrink: 0,
              }}
            >
              <div
                className="absolute top-1 rounded-full bg-white transition-all duration-300"
                style={{
                  width: "20px",
                  height: "20px",
                  left: agentActive ? "28px" : "4px",
                  boxShadow: "0 2px 4px rgba(0,0,0,0.2)",
                }}
              />
            </button>
          </div>

          {agentActive && (
            <div
              className="mt-4 grid grid-cols-3 gap-3"
            >
              {[
                { label: "Consultas hoy", value: "89" },
                { label: "Tiempo resp.", value: "~2s" },
                { label: "Satisfacción", value: "97%" },
              ].map(({ label, value }) => (
                <div key={label} className="rounded-xl p-3 text-center" style={{ background: "#f8fafc" }}>
                  <p style={{ fontSize: "18px", fontWeight: 700, color: "#6366f1" }}>{value}</p>
                  <p style={{ fontSize: "11px", color: "#94a3b8" }}>{label}</p>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Tone selection */}
        <div
          className="rounded-2xl p-5"
          style={{ background: "#fff", border: "1px solid #f1f5f9", boxShadow: "0 1px 8px rgba(0,0,0,0.04)" }}
        >
          <div className="flex items-center gap-2 mb-4">
            <MessageSquare size={16} style={{ color: "#8b5cf6" }} />
            <h3 style={{ fontSize: "14px", fontWeight: 600, color: "#0f172a" }}>
              Tono conversacional
            </h3>
          </div>
          <div className="space-y-2">
            {tones.map((tone) => (
              <button
                key={tone.id}
                onClick={() => setSelectedTone(tone.id)}
                className="w-full flex items-center gap-3 rounded-xl p-4 transition-all text-left"
                style={{
                  background: selectedTone === tone.id ? "rgba(99,102,241,0.06)" : "#f8fafc",
                  border: selectedTone === tone.id ? "1.5px solid rgba(99,102,241,0.35)" : "1.5px solid transparent",
                  cursor: "pointer",
                }}
              >
                <span style={{ fontSize: "22px" }}>{tone.emoji}</span>
                <div className="flex-1">
                  <p style={{ fontSize: "13.5px", fontWeight: 600, color: "#0f172a" }}>{tone.label}</p>
                  <p style={{ fontSize: "12px", color: "#94a3b8" }}>{tone.desc}</p>
                </div>
                {selectedTone === tone.id && (
                  <div
                    className="rounded-full flex items-center justify-center"
                    style={{ width: "20px", height: "20px", background: "#6366f1" }}
                  >
                    <div className="rounded-full bg-white" style={{ width: "8px", height: "8px" }} />
                  </div>
                )}
              </button>
            ))}
          </div>
        </div>

        {/* Schedule */}
        <div
          className="rounded-2xl p-5"
          style={{ background: "#fff", border: "1px solid #f1f5f9", boxShadow: "0 1px 8px rgba(0,0,0,0.04)" }}
        >
          <div className="flex items-center gap-2 mb-4">
            <Clock size={16} style={{ color: "#f59e0b" }} />
            <h3 style={{ fontSize: "14px", fontWeight: 600, color: "#0f172a" }}>
              Horarios de atención
            </h3>
            <div
              className="ml-auto rounded-full px-2 py-0.5"
              style={{ background: "rgba(245,158,11,0.1)", color: "#f59e0b", fontSize: "11px", fontWeight: 600 }}
            >
              Fuera de horario → respuesta automática
            </div>
          </div>

          <div className="space-y-3">
            {schedule.map((slot, i) => (
              <div key={slot.day} className="flex items-center gap-3">
                <button
                  onClick={() => toggleSchedule(i)}
                  className="relative rounded-full transition-all duration-200 shrink-0"
                  style={{
                    width: "40px",
                    height: "22px",
                    background: slot.active ? "#10b981" : "#e2e8f0",
                    border: "none",
                    cursor: "pointer",
                  }}
                >
                  <div
                    className="absolute top-1 rounded-full bg-white transition-all duration-200"
                    style={{ width: "14px", height: "14px", left: slot.active ? "22px" : "4px", boxShadow: "0 1px 3px rgba(0,0,0,0.2)" }}
                  />
                </button>

                <span style={{ fontSize: "13px", fontWeight: 500, color: "#374151", minWidth: "130px" }}>
                  {slot.day}
                </span>

                {slot.active ? (
                  <div className="flex items-center gap-2 flex-1">
                    <input
                      type="time"
                      value={slot.from}
                      className="rounded-lg px-2 py-1 outline-none"
                      style={{ background: "#f8fafc", border: "1px solid #e2e8f0", fontSize: "12.5px", color: "#0f172a" }}
                    />
                    <span style={{ color: "#94a3b8", fontSize: "12px" }}>—</span>
                    <input
                      type="time"
                      value={slot.to}
                      className="rounded-lg px-2 py-1 outline-none"
                      style={{ background: "#f8fafc", border: "1px solid #e2e8f0", fontSize: "12.5px", color: "#0f172a" }}
                    />
                  </div>
                ) : (
                  <span style={{ fontSize: "12.5px", color: "#94a3b8" }}>Cerrado</span>
                )}
              </div>
            ))}
          </div>
        </div>

        {/* Save button */}
        <button
          className="w-full flex items-center justify-center gap-2 rounded-xl py-3"
          style={{ background: "linear-gradient(135deg, #6366f1, #8b5cf6)", color: "#fff", fontSize: "14px", fontWeight: 600, border: "none", cursor: "pointer" }}
        >
          <Settings2 size={16} />
          Guardar configuración del agente
        </button>
      </div>

      {/* Right: Chat simulator */}
      <div
        className="rounded-2xl flex flex-col overflow-hidden"
        style={{ background: "#fff", border: "1px solid #f1f5f9", boxShadow: "0 1px 8px rgba(0,0,0,0.04)", height: "680px" }}
      >
        {/* Chat header */}
        <div
          className="flex items-center gap-3 p-4"
          style={{ borderBottom: "1px solid #f1f5f9" }}
        >
          <div
            className="rounded-xl flex items-center justify-center shrink-0"
            style={{ width: "38px", height: "38px", background: "linear-gradient(135deg, #6366f1, #8b5cf6)" }}
          >
            <Bot size={18} style={{ color: "#fff" }} />
          </div>
          <div>
            <p style={{ fontSize: "13.5px", fontWeight: 600, color: "#0f172a" }}>
              Simulador de agente
            </p>
            <div className="flex items-center gap-1.5">
              <div className="rounded-full" style={{ width: "6px", height: "6px", background: "#10b981" }} />
              <p style={{ fontSize: "11.5px", color: "#10b981" }}>Responde como tu agente configurado</p>
            </div>
          </div>
          <button
            onClick={() => {
              setMessages(initialMessages);
              localStorage.setItem(STORAGE_KEY, JSON.stringify(initialMessages));
            }}
            className="ml-auto rounded-lg p-2 transition-all"
            style={{ background: "#f8fafc", border: "1px solid #e2e8f0", color: "#94a3b8", cursor: "pointer" }}
            title="Reiniciar conversación"
          >
            <RotateCcw size={14} />
          </button>
        </div>

        {/* Tone indicator */}
        <div
          className="flex items-center gap-2 px-4 py-2"
          style={{ background: "rgba(99,102,241,0.04)", borderBottom: "1px solid rgba(99,102,241,0.08)" }}
        >
          <Sparkles size={12} style={{ color: "#8b5cf6" }} />
          <span style={{ fontSize: "11.5px", color: "#8b5cf6", fontWeight: 500 }}>
            Tono activo: {tones.find(t => t.id === selectedTone)?.label} {tones.find(t => t.id === selectedTone)?.emoji}
          </span>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.map((msg, i) => (
            <div
              key={i}
              className={`flex items-end gap-2 ${msg.role === "user" ? "flex-row-reverse" : "flex-row"}`}
            >
              {/* Avatar */}
              <div
                className="rounded-full flex items-center justify-center shrink-0"
                style={{
                  width: "28px",
                  height: "28px",
                  background: msg.role === "agent"
                    ? "linear-gradient(135deg, #6366f1, #8b5cf6)"
                    : "#e2e8f0",
                }}
              >
                {msg.role === "agent" ? (
                  <Bot size={14} style={{ color: "#fff" }} />
                ) : (
                  <User size={14} style={{ color: "#64748b" }} />
                )}
              </div>

              {/* Bubble */}
              <div
                className="rounded-2xl px-4 py-3 max-w-xs"
                style={{
                  background: msg.role === "agent"
                    ? "#f8fafc"
                    : "linear-gradient(135deg, #6366f1, #8b5cf6)",
                  border: msg.role === "agent" ? "1px solid #f1f5f9" : "none",
                  borderBottomLeftRadius: msg.role === "agent" ? "4px" : "16px",
                  borderBottomRightRadius: msg.role === "user" ? "4px" : "16px",
                }}
              >
                <div>
                  {renderMessageText(msg.text, msg.role)}
                </div>
                <div
                  style={{
                    fontSize: "11px",
                    color: msg.role === "agent" ? "#94a3b8" : "rgba(255,255,255,0.7)",
                    marginTop: "6px",
                  }}
                >
                  {msg.time}
                </div>
              </div>
            </div>
          ))}
          {isTyping && (
            <div className="flex items-end gap-2">
              <div
                className="rounded-full flex items-center justify-center shrink-0"
                style={{
                  width: "28px",
                  height: "28px",
                  background: "linear-gradient(135deg, #6366f1, #8b5cf6)",
                }}
              >
                <Bot size={14} style={{ color: "#fff" }} />
              </div>
              <div
                className="rounded-2xl px-4 py-3"
                style={{
                  background: "#f8fafc",
                  border: "1px solid #f1f5f9",
                  borderBottomLeftRadius: "4px",
                }}
              >
                <div className="flex gap-1">
                  {[0, 1, 2].map((i) => (
                    <div
                      key={i}
                      style={{
                        width: "6px",
                        height: "6px",
                        borderRadius: "50%",
                        background: "#cbd5e1",
                        animation: `bounce 1.4s infinite`,
                        animationDelay: `${i * 0.2}s`,
                      }}
                    />
                  ))}
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Quick replies */}
        <div className="px-4 py-2 flex gap-2 overflow-x-auto" style={{ borderTop: "1px solid #f8fafc" }}>
          {["¿Tienen envío gratis?", "¿Cuánto tardan en entregar?", "Ver catálogo", "Rastrear pedido"].map((q) => (
            <button
              key={q}
              onClick={() => {
                setInputText(q);
              }}
              className="rounded-full px-3 py-1.5 whitespace-nowrap"
              style={{
                background: "rgba(99,102,241,0.08)",
                border: "1px solid rgba(99,102,241,0.2)",
                color: "#6366f1",
                fontSize: "12px",
                fontWeight: 500,
                cursor: "pointer",
              }}
            >
              {q}
            </button>
          ))}
        </div>

        {/* Input */}
        <div className="p-4 pt-2">
          {error && (
            <div
              className="rounded-xl px-3 py-2 mb-2"
              style={{ background: "rgba(239,68,68,0.08)", border: "1px solid rgba(239,68,68,0.25)" }}
            >
              <p style={{ fontSize: "12px", color: "#b91c1c", fontWeight: 500 }}>{error}</p>
            </div>
          )}

          <div
            className="flex gap-3 rounded-2xl p-4"
            style={{ background: "#f8fafc", border: "1.5px solid #e2e8f0" }}
          >
            <textarea
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Escribe tu mensaje (Enter para saltar línea, Ctrl+Enter para enviar)..."
              className="flex-1 outline-none bg-transparent resize-none"
              style={{
                fontSize: "13.5px",
                color: "#0f172a",
                fontFamily: "system-ui, -apple-system, sans-serif",
                lineHeight: 1.5,
                maxHeight: "120px",
              }}
              rows={3}
            />
            <button
              onClick={handleSend}
              disabled={!inputText.trim()}
              className="rounded-xl flex items-center justify-center transition-all shrink-0"
              style={{
                width: "40px",
                height: "40px",
                background: inputText.trim() ? "linear-gradient(135deg, #6366f1, #8b5cf6)" : "#e2e8f0",
                border: "none",
                cursor: inputText.trim() ? "pointer" : "not-allowed",
              }}
              title="Ctrl+Enter para enviar"
            >
              <Send size={16} style={{ color: inputText.trim() ? "#fff" : "#94a3b8" }} />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
