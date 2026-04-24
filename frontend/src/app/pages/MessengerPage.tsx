import { useState, useEffect } from "react";
import {
  CheckCircle2,
  AlertCircle,
  Copy,
  RefreshCw,
  Wifi,
  WifiOff,
  Info,
} from "lucide-react";
import { api, ApiError } from "../lib/api";

interface MessengerConnection {
  is_connected: boolean;
  page_id: string;
  page_name: string | null;
  page_access_token: string;
  verify_token: string;
}

export function MessengerPage() {
  const [connected, setConnected] = useState(false);
  const [connecting, setConnecting] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [form, setForm] = useState({
    pageId: "",
    pageName: "",
    pageAccessToken: "",
    verifyToken: "",
  });
  const [copiedField, setCopiedField] = useState<string | null>(null);

  // Cargar credenciales guardadas al montar el componente
  useEffect(() => {
    const loadMessengerConnection = async () => {
      try {
        setLoading(true);
        const data = await api.get(
          "/messenger/me",
          true
        ) as MessengerConnection;
        
        if (data.is_connected) {
          setConnected(true);
          setForm({
            pageId: data.page_id || "",
            pageName: data.page_name || "",
            pageAccessToken: data.page_access_token || "",
            verifyToken: data.verify_token || "",
          });
        }
      } catch (err) {
        // No hay conexión guardada aún, es normal
        if (err instanceof ApiError && err.status !== 404) {
          setError("No se pudo cargar la configuración de Messenger");
        }
      } finally {
        setLoading(false);
      }
    };

    loadMessengerConnection();
  }, []);

  const handleCopy = (field: string, value: string) => {
    navigator.clipboard.writeText(value).catch(() => {});    
    setCopiedField(field);
    setTimeout(() => setCopiedField(null), 2000);
  };

  const handleConnect = async () => {
    // Validar campos requeridos
    if (!form.pageId.trim()) {
      setError("El Page ID es requerido");
      return;
    }
    if (!form.pageAccessToken.trim()) {
      setError("El Access Token es requerido");
      return;
    }
    if (!form.verifyToken.trim()) {
      setError("El Verify Token es requerido");
      return;
    }

    setConnecting(true);
    setError("");
    setSuccess("");

    try {
      const response = await api.put(
        "/messenger/me",
        {
          page_id: form.pageId,
          page_name: form.pageName || null,
          page_access_token: form.pageAccessToken,
          verify_token: form.verifyToken,
        },
        true
      ) as MessengerConnection;

      if (response.is_connected) {
        setConnected(true);
        setSuccess("✅ Conexión de Messenger guardada exitosamente");
        setTimeout(() => setSuccess(""), 3000);
      }
    } catch (err) {
      const message =
        err instanceof ApiError
          ? err.detail
          : "Error al guardar la configuración";
      setError(message);
    } finally {
      setConnecting(false);
    }
  };

  const handleDisconnect = async () => {
    setConnecting(true);
    setError("");

    try {
      await api.put(
        "/messenger/me",
        {
          page_id: form.pageId,
          page_name: form.pageName || null,
          page_access_token: form.pageAccessToken,
          verify_token: form.verifyToken,
          is_connected: false,
        },
        true
      );
      setConnected(false);
      setSuccess("Desconexión exitosa");
      setTimeout(() => setSuccess(""), 3000);
    } catch (err) {
      const message =
        err instanceof ApiError
          ? err.detail
          : "Error al desconectar";
      setError(message);
    } finally {
      setConnecting(false);
    }
  };

  return (
    <div className="space-y-5 max-w-5xl">
      {/* Loading state */}
      {loading && (
        <div
          className="rounded-2xl p-4 flex items-center gap-3"
          style={{ background: "rgba(59,89,152, 0.08)", border: "1px solid rgba(59,89,152, 0.2)" }}
        >
          <RefreshCw size={16} style={{ color: "#3b5998", animation: "spin 1s linear infinite" }} />
          <span style={{ fontSize: "13px", color: "#3b5998", fontWeight: 500 }}>
            Cargando configuración de Messenger...
          </span>
        </div>
      )}

      {/* Error message */}
      {error && (
        <div
          className="rounded-2xl p-4 flex items-center gap-3"
          style={{ background: "rgba(239,68,68,0.08)", border: "1px solid rgba(239,68,68,0.2)" }}
        >
          <AlertCircle size={16} style={{ color: "#ef4444" }} />
          <span style={{ fontSize: "13px", color: "#b91c1c", fontWeight: 500 }}>
            {error}
          </span>
        </div>
      )}

      {/* Success message */}
      {success && (
        <div
          className="rounded-2xl p-4 flex items-center gap-3"
          style={{ background: "rgba(16,185,129,0.08)", border: "1px solid rgba(16,185,129,0.2)" }}
        >
          <CheckCircle2 size={16} style={{ color: "#10b981" }} />
          <span style={{ fontSize: "13px", color: "#047857", fontWeight: 500 }}>
            {success}
          </span>
        </div>
      )}

      {/* Connection Status Card */}
      <div
        className="rounded-2xl p-6"
        style={{
          background: connected ? "rgba(16,185,129,0.05)" : "rgba(107,114,128,0.05)",
          border: connected ? "1px solid rgba(16,185,129,0.2)" : "1px solid rgba(107,114,128,0.2)",
        }}
      >
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-3">
            {connected ? (
              <Wifi size={24} style={{ color: "#10b981" }} />
            ) : (
              <WifiOff size={24} style={{ color: "#9ca3af" }} />
            )}
            <div>
              <h2 style={{ fontSize: "18px", fontWeight: 600, margin: 0 }}>
                Conexión de Messenger
              </h2>
              <p style={{ fontSize: "12px", color: "#6b7280", margin: 0, marginTop: "4px" }}>
                {connected ? (
                  <span style={{ color: "#10b981" }}>✅ Conectado</span>
                ) : (
                  "⚠️ No conectado"
                )}
              </p>
            </div>
          </div>
          {connected && (
            <button
              onClick={handleDisconnect}
              disabled={connecting}
              style={{
                padding: "8px 16px",
                background: "#ef4444",
                color: "white",
                border: "none",
                borderRadius: "8px",
                cursor: connecting ? "default" : "pointer",
                opacity: connecting ? 0.6 : 1,
                fontSize: "13px",
                fontWeight: 500,
              }}
            >
              {connecting ? "Desconectando..." : "Desconectar"}
            </button>
          )}
        </div>
      </div>

      {/* Configuration Form */}
      <div className="rounded-2xl p-6" style={{ background: "#f9fafb", border: "1px solid #e5e7eb" }}>
        <h3 style={{ fontSize: "16px", fontWeight: 600, marginBottom: "16px", margin: 0 }}>
          Configuración de Messenger
        </h3>

        {/* Page ID */}
        <div style={{ marginBottom: "16px" }}>
          <label style={{ fontSize: "13px", fontWeight: 500, color: "#374151", display: "block", marginBottom: "6px" }}>
            Page ID
          </label>
          <div style={{ display: "flex", gap: "8px" }}>
            <input
              type="text"
              placeholder="Ej: 123456789123456"
              value={form.pageId}
              onChange={(e) => setForm({ ...form, pageId: e.target.value })}
              disabled={connected}
              style={{
                flex: 1,
                padding: "10px 12px",
                border: "1px solid #d1d5db",
                borderRadius: "8px",
                fontSize: "13px",
                fontFamily: "monospace",
              }}
            />
            {form.pageId && (
              <button
                onClick={() => handleCopy("pageId", form.pageId)}
                style={{
                  padding: "10px 12px",
                  background: copiedField === "pageId" ? "#10b981" : "#f3f4f6",
                  color: copiedField === "pageId" ? "white" : "#6b7280",
                  border: "1px solid #d1d5db",
                  borderRadius: "8px",
                  cursor: "pointer",
                }}
              >
                {copiedField === "pageId" ? <CheckCircle2 size={16} /> : <Copy size={16} />}
              </button>
            )}
          </div>
        </div>

        {/* Page Name */}
        <div style={{ marginBottom: "16px" }}>
          <label style={{ fontSize: "13px", fontWeight: 500, color: "#374151", display: "block", marginBottom: "6px" }}>
            Nombre de Página (Opcional)
          </label>
          <input
            type="text"
            placeholder="Ej: Mi Tienda Online"
            value={form.pageName}
            onChange={(e) => setForm({ ...form, pageName: e.target.value })}
            disabled={connected}
            style={{
              width: "100%",
              padding: "10px 12px",
              border: "1px solid #d1d5db",
              borderRadius: "8px",
              fontSize: "13px",
            }}
          />
        </div>

        {/* Page Access Token */}
        <div style={{ marginBottom: "16px" }}>
          <label style={{ fontSize: "13px", fontWeight: 500, color: "#374151", display: "block", marginBottom: "6px" }}>
            Access Token de Página
          </label>
          <textarea
            placeholder="Pega tu token de acceso de la página aquí...  EAA..."
            value={form.pageAccessToken}
            onChange={(e) => setForm({ ...form, pageAccessToken: e.target.value })}
            disabled={connected}
            style={{
              width: "100%",
              padding: "12px",
              border: "1px solid #d1d5db",
              borderRadius: "8px",
              fontSize: "12px",
              fontFamily: "monospace",
              minHeight: "80px",
              fontWeight: 200,
            }}
          />
        </div>

        {/* Verify Token */}
        <div style={{ marginBottom: "16px" }}>
          <label style={{ fontSize: "13px", fontWeight: 500, color: "#374151", display: "block", marginBottom: "6px" }}>
            Verify Token (Tu Token Secreto)
          </label>
          <input
            type="text"
            placeholder="Ej: mi_token_secreto_2024"
            value={form.verifyToken}
            onChange={(e) => setForm({ ...form, verifyToken: e.target.value })}
            disabled={connected}
            style={{
              width: "100%",
              padding: "10px 12px",
              border: "1px solid #d1d5db",
              borderRadius: "8px",
              fontSize: "13px",
            }}
          />
        </div>

        {/* Info Box */}
        <div
          style={{
            background: "rgba(59,89,152, 0.08)",
            border: "1px solid rgba(59,89,152, 0.2)",
            borderRadius: "8px",
            padding: "12px",
            marginBottom: "16px",
            display: "flex",
            gap: "10px",
          }}
        >
          <Info size={16} style={{ color: "#3b5998", flexShrink: 0, marginTop: "2px" }} />
          <div style={{ fontSize: "12px", color: "#1f2937" }}>
            <p style={{ margin: 0, fontWeight: 600, marginBottom: "4px" }}>Cómo obtener estos datos:</p>
            <ol style={{ margin: 0, paddingLeft: "20px", fontSize: "12px" }}>
              <li>Ve a fb.com/me/pages</li>
              <li>Selecciona tu página de negocio</li>
              <li>Ve a Configuración → Integración → Meta App</li>
              <li>Genera un Access Token con permisos de Messenger</li>
              <li>El Verify Token es cualquier string que tú elijas (cópialo para usarlo después)</li>
            </ol>
          </div>
        </div>

        {/* Connect Button */}
        <button
          onClick={handleConnect}
          disabled={connecting || connected}
          style={{
            width: "100%",
            padding: "12px",
            background: connected ? "#d1d5db" : "#3b5998",
            color: "white",
            border: "none",
            borderRadius: "8px",
            cursor: connected || connecting ? "default" : "pointer",
            fontSize: "14px",
            fontWeight: 600,
            opacity: (connected || connecting) ? 0.6 : 1,
          }}
        >
          {connecting ? "Conectando..." : connected ? "Conectado ✅" : "Conectar Messenger"}
        </button>
      </div>

      {/* Webhook Configuration Instructions */}
      {connected && (
        <div className="rounded-2xl p-6" style={{ background: "#fef3c7", border: "1px solid #fcd34d" }}>
          <h3 style={{ fontSize: "16px", fontWeight: 600, marginBottom: "12px", margin: 0, color: "#92400e" }}>
            📋 Últimos Pasos para Configurar el Webhook
          </h3>
          <ol style={{ marginBottom: 0, paddingLeft: "20px", color: "#92400e", fontSize: "13px" }}>
            <li style={{ marginBottom: "8px" }}>
              Ve a tu app en{" "}
              <a href="https://developers.facebook.com/apps" target="_blank" rel="noreferrer" style={{ color: "#b45309" }}>
                Developers Facebook
              </a>
            </li>
            <li style={{ marginBottom: "8px" }}>
              Messenger → Configuración → Configurar Webhooks
            </li>
            <li style={{ marginBottom: "8px" }}>
              Webhook URL: <code style={{ background: "white", padding: "2px 6px" }}>https://tu-dominio.com/messenger/webhook</code>
            </li>
            <li style={{ marginBottom: "8px" }}>
              Verify Token: <code style={{ background: "white", padding: "2px 6px" }}>{form.verifyToken}</code>
            </li>
            <li>Marca los eventos: messages, message_echoes, messaging_postbacks</li>
          </ol>
        </div>
      )}
    </div>
  );
}
