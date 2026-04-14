import { useState } from "react";
import {
  MessageCircle,
  Shield,
  CheckCircle2,
  AlertCircle,
  Copy,
  ExternalLink,
  RefreshCw,
  Wifi,
  WifiOff,
  Phone,
  QrCode,
  ChevronRight,
  Info,
} from "lucide-react";

const mockMessages = [
  { from: "María López", phone: "+52 55 1234 5678", text: "Hola! ¿Tienen el vestido en talla M?", time: "10:32", avatar: "ML" },
  { from: "Carlos R.", phone: "+52 33 9876 5432", text: "Mi pedido no ha llegado, folio #4820", time: "10:18", avatar: "CR" },
  { from: "Ana García", phone: "+52 81 4567 8901", text: "¿Cuánto cuesta el envío a Monterrey?", time: "09:55", avatar: "AG" },
  { from: "Luis M.", phone: "+52 55 2345 6789", text: "Gracias por mi pedido, todo perfecto ⭐", time: "09:40", avatar: "LM" },
  { from: "Sofía Ruiz", phone: "+52 33 3456 7890", text: "¿Aceptan pagos con tarjeta?", time: "09:12", avatar: "SR" },
];

const stats = [
  { label: "Mensajes hoy", value: "234", color: "#6366f1" },
  { label: "Respondidos", value: "218", color: "#10b981" },
  { label: "Pendientes", value: "16", color: "#f59e0b" },
  { label: "Tasa respuesta", value: "93%", color: "#3b82f6" },
];

export function WhatsAppPage() {
  const [connected, setConnected] = useState(true);
  const [connecting, setConnecting] = useState(false);
  const [form, setForm] = useState({
    phoneNumber: "+52 1 (55) 1234-5678",
    accessToken: "EAABxxxxxxxxxxxxxxxx",
    phoneNumberId: "1234567890",
    businessAccountId: "0987654321",
    webhookToken: "mi_token_secreto_123",
  });
  const [activeTab, setActiveTab] = useState<"conexion" | "mensajes" | "plantillas">("conexion");
  const [copiedField, setCopiedField] = useState<string | null>(null);

  const handleCopy = (field: string, value: string) => {
    navigator.clipboard.writeText(value).catch(() => {});    
    setCopiedField(field);
    setTimeout(() => setCopiedField(null), 2000);
  };

  const handleConnect = () => {
    setConnecting(true);
    setTimeout(() => {
      setConnecting(false);
      setConnected(true);
    }, 2000);
  };

  const handleDisconnect = () => {
    setConnected(false);
  };

  return (
    <div className="space-y-5 max-w-5xl">
      {/* Status banner */}
      <div
        className="rounded-2xl p-5 flex items-center gap-4"
        style={{
          background: connected
            ? "linear-gradient(135deg, rgba(16,185,129,0.08), rgba(52,211,153,0.05))"
            : "linear-gradient(135deg, rgba(239,68,68,0.08), rgba(252,165,165,0.05))",
          border: connected ? "1px solid rgba(16,185,129,0.2)" : "1px solid rgba(239,68,68,0.2)",
        }}
      >
        <div
          className="rounded-2xl flex items-center justify-center shrink-0"
          style={{
            width: "56px",
            height: "56px",
            background: connected ? "#25D366" : "#ef4444",
          }}
        >
          <MessageCircle size={26} style={{ color: "#fff" }} />
        </div>
        <div className="flex-1">
          <div className="flex items-center gap-2 mb-1">
            <h3 style={{ fontSize: "16px", fontWeight: 700, color: "#0f172a" }}>
              WhatsApp Business API
            </h3>
            <div
              className="flex items-center gap-1.5 rounded-full px-2.5 py-0.5"
              style={{
                background: connected ? "rgba(16,185,129,0.15)" : "rgba(239,68,68,0.15)",
                color: connected ? "#10b981" : "#ef4444",
              }}
            >
              <div
                className="rounded-full"
                style={{ width: "6px", height: "6px", background: connected ? "#10b981" : "#ef4444" }}
              />
              <span style={{ fontSize: "11.5px", fontWeight: 700 }}>
                {connected ? "Conectado" : "Desconectado"}
              </span>
            </div>
          </div>
          <p style={{ fontSize: "13px", color: "#64748b" }}>
            {connected
              ? `Número activo: ${form.phoneNumber} · Integración Meta Cloud API v18`
              : "Configura tus credenciales de Meta para conectar WhatsApp Business"}
          </p>
        </div>
        <div className="flex items-center gap-3">
          {connected ? (
            <>
              <button
                onClick={handleDisconnect}
                className="rounded-xl px-4 py-2.5 flex items-center gap-2"
                style={{ background: "#fff", border: "1.5px solid rgba(239,68,68,0.3)", color: "#ef4444", fontSize: "13px", fontWeight: 600, cursor: "pointer" }}
              >
                <WifiOff size={14} />
                Desconectar
              </button>
              <button
                className="rounded-xl px-4 py-2.5 flex items-center gap-2"
                style={{ background: "#25D366", color: "#fff", border: "none", fontSize: "13px", fontWeight: 600, cursor: "pointer" }}
              >
                <Wifi size={14} />
                Reconectar
              </button>
            </>
          ) : (
            <button
              onClick={handleConnect}
              disabled={connecting}
              className="rounded-xl px-5 py-2.5 flex items-center gap-2"
              style={{
                background: connecting ? "#e2e8f0" : "#25D366",
                color: connecting ? "#94a3b8" : "#fff",
                border: "none",
                fontSize: "13px",
                fontWeight: 600,
                cursor: connecting ? "not-allowed" : "pointer",
              }}
            >
              {connecting ? (
                <>
                  <RefreshCw size={14} className="animate-spin" />
                  Conectando...
                </>
              ) : (
                <>
                  <Wifi size={14} />
                  Conectar ahora
                </>
              )}
            </button>
          )}
        </div>
      </div>

      {/* Stats */}
      {connected && (
        <div className="grid grid-cols-4 gap-4">
          {stats.map(({ label, value, color }) => (
            <div
              key={label}
              className="rounded-2xl p-4"
              style={{ background: "#fff", border: "1px solid #f1f5f9", boxShadow: "0 1px 8px rgba(0,0,0,0.04)" }}
            >
              <p style={{ fontSize: "26px", fontWeight: 700, color, letterSpacing: "-0.5px" }}>{value}</p>
              <p style={{ fontSize: "12.5px", color: "#94a3b8", marginTop: "2px" }}>{label}</p>
            </div>
          ))}
        </div>
      )}

      {/* Tabs */}
      <div className="flex gap-1 p-1 rounded-xl" style={{ background: "#f1f5f9", width: "fit-content" }}>
        {(["conexion", "mensajes", "plantillas"] as const).map((tab) => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            className="rounded-lg px-5 py-2 transition-all"
            style={{
              background: activeTab === tab ? "#fff" : "transparent",
              color: activeTab === tab ? "#0f172a" : "#64748b",
              fontSize: "13px",
              fontWeight: activeTab === tab ? 600 : 500,
              border: "none",
              cursor: "pointer",
              boxShadow: activeTab === tab ? "0 1px 4px rgba(0,0,0,0.08)" : "none",
              textTransform: "capitalize",
            }}
          >
            {tab === "conexion" ? "Configuración" : tab.charAt(0).toUpperCase() + tab.slice(1)}
          </button>
        ))}
      </div>

      {/* Tab content */}
      {activeTab === "conexion" && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">
          {/* Credentials form */}
          <div
            className="rounded-2xl p-5"
            style={{ background: "#fff", border: "1px solid #f1f5f9", boxShadow: "0 1px 8px rgba(0,0,0,0.04)" }}
          >
            <div className="flex items-center gap-2 mb-5">
              <Shield size={16} style={{ color: "#6366f1" }} />
              <h3 style={{ fontSize: "14px", fontWeight: 600, color: "#0f172a" }}>
                Credenciales de Meta API
              </h3>
            </div>

            <div className="space-y-4">
              {[
                { label: "Número de teléfono", field: "phoneNumber", hint: "Formato: +52 1 55 XXXX XXXX" },
                { label: "Access Token", field: "accessToken", hint: "Token permanente de Meta for Developers" },
                { label: "Phone Number ID", field: "phoneNumberId", hint: "ID del número en Meta Business" },
                { label: "Business Account ID", field: "businessAccountId", hint: "ID de tu cuenta de WhatsApp Business" },
                { label: "Webhook Verify Token", field: "webhookToken", hint: "Token para verificar tu webhook" },
              ].map(({ label, field, hint }) => (
                <div key={field}>
                  <label className="block mb-1.5" style={{ fontSize: "12.5px", fontWeight: 600, color: "#475569" }}>
                    {label}
                  </label>
                  <div className="relative">
                    <input
                      type={field === "accessToken" ? "password" : "text"}
                      value={form[field as keyof typeof form]}
                      onChange={(e) => setForm((prev) => ({ ...prev, [field]: e.target.value }))}
                      className="w-full rounded-xl px-4 py-2.5 outline-none pr-12"
                      style={{ background: "#f8fafc", border: "1.5px solid #e2e8f0", fontSize: "13px", color: "#0f172a", fontFamily: field !== "phoneNumber" ? "monospace" : "inherit" }}
                    />
                    <button
                      onClick={() => handleCopy(field, form[field as keyof typeof form])}
                      className="absolute right-3 top-1/2 -translate-y-1/2 rounded-lg p-1"
                      style={{ background: "transparent", border: "none", cursor: "pointer", color: copiedField === field ? "#10b981" : "#94a3b8" }}
                    >
                      {copiedField === field ? <CheckCircle2 size={14} /> : <Copy size={14} />}
                    </button>
                  </div>
                  <p style={{ fontSize: "11px", color: "#94a3b8", marginTop: "4px" }}>{hint}</p>
                </div>
              ))}
            </div>

            <button
              onClick={handleConnect}
              className="mt-5 w-full flex items-center justify-center gap-2 rounded-xl py-3"
              style={{ background: "#25D366", color: "#fff", border: "none", fontSize: "13.5px", fontWeight: 600, cursor: "pointer" }}
            >
              <CheckCircle2 size={16} />
              Guardar y verificar conexión
            </button>
          </div>

          {/* Right panel */}
          <div className="space-y-4">
            {/* Setup guide */}
            <div
              className="rounded-2xl p-5"
              style={{ background: "#fff", border: "1px solid #f1f5f9", boxShadow: "0 1px 8px rgba(0,0,0,0.04)" }}
            >
              <div className="flex items-center gap-2 mb-4">
                <Info size={16} style={{ color: "#f59e0b" }} />
                <h3 style={{ fontSize: "14px", fontWeight: 600, color: "#0f172a" }}>
                  Guía de configuración
                </h3>
              </div>
              <div className="space-y-3">
                {[
                  { step: "1", title: "Crea una app en Meta for Developers", done: true },
                  { step: "2", title: "Agrega el producto WhatsApp Business API", done: true },
                  { step: "3", title: "Obtén el Access Token permanente", done: true },
                  { step: "4", title: "Configura el webhook en DropSync", done: connected },
                  { step: "5", title: "Verifica el número de teléfono", done: connected },
                ].map(({ step, title, done }) => (
                  <div key={step} className="flex items-center gap-3">
                    <div
                      className="rounded-full flex items-center justify-center shrink-0"
                      style={{
                        width: "26px",
                        height: "26px",
                        background: done ? "rgba(16,185,129,0.15)" : "#f1f5f9",
                        color: done ? "#10b981" : "#94a3b8",
                        fontSize: "12px",
                        fontWeight: 700,
                      }}
                    >
                      {done ? <CheckCircle2 size={14} /> : step}
                    </div>
                    <p style={{ fontSize: "13px", color: done ? "#374151" : "#94a3b8", fontWeight: done ? 500 : 400 }}>
                      {title}
                    </p>
                  </div>
                ))}
              </div>
              <a
                href="#"
                className="flex items-center gap-2 mt-4"
                style={{ color: "#6366f1", fontSize: "12.5px", fontWeight: 600 }}
              >
                <ExternalLink size={13} />
                Ver documentación completa de Meta
              </a>
            </div>

            {/* Webhook info */}
            <div
              className="rounded-2xl p-5"
              style={{ background: "#fff", border: "1px solid #f1f5f9", boxShadow: "0 1px 8px rgba(0,0,0,0.04)" }}
            >
              <div className="flex items-center gap-2 mb-4">
                <QrCode size={16} style={{ color: "#8b5cf6" }} />
                <h3 style={{ fontSize: "14px", fontWeight: 600, color: "#0f172a" }}>
                  URL del Webhook
                </h3>
              </div>
              <div
                className="rounded-xl p-3 flex items-center justify-between"
                style={{ background: "#0f172a" }}
              >
                <code style={{ fontSize: "11.5px", color: "#a5b4fc", fontFamily: "monospace" }}>
                  https://api.dropsync.io/webhook/wa/tu-empresa
                </code>
                <button
                  onClick={() => handleCopy("webhook", "https://api.dropsync.io/webhook/wa/tu-empresa")}
                  className="rounded-lg p-1.5"
                  style={{ background: "rgba(255,255,255,0.08)", border: "none", cursor: "pointer", color: "#94a3b8" }}
                >
                  {copiedField === "webhook" ? <CheckCircle2 size={13} style={{ color: "#10b981" }} /> : <Copy size={13} />}
                </button>
              </div>
              <p style={{ fontSize: "11px", color: "#94a3b8", marginTop: "8px" }}>
                Agrega esta URL en la configuración de webhook de tu app en Meta for Developers
              </p>
            </div>
          </div>
        </div>
      )}

      {activeTab === "mensajes" && (
        <div
          className="rounded-2xl overflow-hidden"
          style={{ background: "#fff", border: "1px solid #f1f5f9", boxShadow: "0 1px 8px rgba(0,0,0,0.04)" }}
        >
          <div className="p-4" style={{ borderBottom: "1px solid #f1f5f9" }}>
            <h3 style={{ fontSize: "14px", fontWeight: 600, color: "#0f172a" }}>
              Mensajes recientes
            </h3>
          </div>
          <div className="divide-y divide-slate-50">
            {mockMessages.map((msg) => (
              <div
                key={msg.phone}
                className="flex items-center gap-4 px-4 py-4 cursor-pointer transition-all"
                onMouseEnter={(e) => (e.currentTarget.style.background = "#fafbfc")}
                onMouseLeave={(e) => (e.currentTarget.style.background = "transparent")}
              >
                <div
                  className="rounded-full flex items-center justify-center shrink-0"
                  style={{ width: "42px", height: "42px", background: "linear-gradient(135deg, #25D366, #128C7E)" }}
                >
                  <span style={{ color: "#fff", fontSize: "13px", fontWeight: 700 }}>{msg.avatar}</span>
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2">
                    <p style={{ fontSize: "14px", fontWeight: 600, color: "#0f172a" }}>{msg.from}</p>
                    <span style={{ fontSize: "11.5px", color: "#94a3b8" }}>{msg.phone}</span>
                  </div>
                  <p style={{ fontSize: "13px", color: "#64748b", overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
                    {msg.text}
                  </p>
                </div>
                <div className="flex flex-col items-end gap-2">
                  <span style={{ fontSize: "11.5px", color: "#94a3b8" }}>{msg.time}</span>
                  <ChevronRight size={14} style={{ color: "#cbd5e1" }} />
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {activeTab === "plantillas" && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
          {[
            {
              name: "Confirmación de pedido",
              status: "aprobada",
              text: "Hola {{1}}, tu pedido {{2}} ha sido confirmado. El total es ${{3}}. Te notificaremos cuando sea enviado. 📦",
            },
            {
              name: "Notificación de envío",
              status: "aprobada",
              text: "¡Buenas noticias {{1}}! Tu pedido {{2}} está en camino 🚚. Número de rastreo: {{3}}. Llegará en 3-5 días hábiles.",
            },
            {
              name: "Mensaje de bienvenida",
              status: "aprobada",
              text: "¡Bienvenido a Mi Moda Online! 👋 Soy tu asistente virtual. ¿En qué puedo ayudarte hoy? Tenemos más de 1,200 productos disponibles.",
            },
            {
              name: "Recuperación carrito",
              status: "pendiente",
              text: "Hola {{1}}, notamos que dejaste productos en tu carrito. ¿Te gustaría completar tu compra? Te esperamos. 🛍️",
            },
          ].map((tpl) => (
            <div
              key={tpl.name}
              className="rounded-2xl p-5"
              style={{ background: "#fff", border: "1px solid #f1f5f9", boxShadow: "0 1px 8px rgba(0,0,0,0.04)" }}
            >
              <div className="flex items-center justify-between mb-3">
                <h4 style={{ fontSize: "14px", fontWeight: 600, color: "#0f172a" }}>{tpl.name}</h4>
                <div
                  className="rounded-full px-2.5 py-1"
                  style={{
                    background: tpl.status === "aprobada" ? "rgba(16,185,129,0.1)" : "rgba(245,158,11,0.1)",
                    color: tpl.status === "aprobada" ? "#10b981" : "#f59e0b",
                    fontSize: "11px",
                    fontWeight: 600,
                  }}
                >
                  {tpl.status === "aprobada" ? "✓ Aprobada" : "⏳ Pendiente"}
                </div>
              </div>
              <div
                className="rounded-xl p-4"
                style={{ background: "#f8fafc", border: "1px solid #f1f5f9" }}
              >
                <p style={{ fontSize: "13px", color: "#374151", lineHeight: 1.6 }}>{tpl.text}</p>
              </div>
              <div className="flex gap-2 mt-3">
                <button
                  className="flex-1 rounded-lg py-2 text-center"
                  style={{ background: "rgba(99,102,241,0.08)", color: "#6366f1", fontSize: "12.5px", fontWeight: 600, border: "none", cursor: "pointer" }}
                >
                  Usar plantilla
                </button>
                <button
                  className="rounded-lg px-3 py-2"
                  style={{ background: "#f8fafc", border: "1px solid #e2e8f0", color: "#64748b", fontSize: "12.5px", cursor: "pointer" }}
                >
                  Editar
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
