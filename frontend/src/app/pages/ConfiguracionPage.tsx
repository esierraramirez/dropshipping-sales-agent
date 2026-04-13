import { useState } from "react";
import {
  User,
  Bell,
  Shield,
  CreditCard,
  Palette,
  Globe,
  Key,
  Save,
  ChevronRight,
  Eye,
  EyeOff,
  CheckCircle2,
  Zap,
} from "lucide-react";

const sections = [
  { id: "perfil", icon: User, label: "Perfil de usuario" },
  { id: "notificaciones", icon: Bell, label: "Notificaciones" },
  { id: "seguridad", icon: Shield, label: "Seguridad" },
  { id: "suscripcion", icon: CreditCard, label: "Suscripción y facturación" },
  { id: "apariencia", icon: Palette, label: "Apariencia" },
  { id: "integraciones", icon: Globe, label: "Integraciones" },
];

function Toggle({ value, onChange }: { value: boolean; onChange: (v: boolean) => void }) {
  return (
    <button
      onClick={() => onChange(!value)}
      className="relative rounded-full transition-all duration-200 shrink-0"
      style={{ width: "44px", height: "24px", background: value ? "linear-gradient(135deg, #6366f1, #8b5cf6)" : "#e2e8f0", border: "none", cursor: "pointer" }}
    >
      <div
        className="absolute top-1 rounded-full bg-white transition-all duration-200"
        style={{ width: "16px", height: "16px", left: value ? "24px" : "4px", boxShadow: "0 1px 3px rgba(0,0,0,0.2)" }}
      />
    </button>
  );
}

export function ConfiguracionPage() {
  const [activeSection, setActiveSection] = useState("perfil");
  const [showCurrentPw, setShowCurrentPw] = useState(false);
  const [showNewPw, setShowNewPw] = useState(false);
  const [saved, setSaved] = useState(false);

  const [notifications, setNotifications] = useState({
    newOrder: true,
    orderStatus: true,
    whatsappMessages: false,
    agentAlerts: true,
    weeklyReport: true,
    marketingEmails: false,
    smsAlerts: false,
  });

  const [profile, setProfile] = useState({
    nombre: "Juan García",
    email: "juan@mimoda.mx",
    telefono: "+52 55 1234 5678",
    zona: "America/Mexico_City",
    idioma: "Español (México)",
  });

  const handleSave = () => {
    setSaved(true);
    setTimeout(() => setSaved(false), 3000);
  };

  const toggleNotification = (key: keyof typeof notifications) => {
    setNotifications((prev) => ({ ...prev, [key]: !prev[key] }));
  };

  return (
    <div className="flex gap-5 max-w-5xl">
      {/* Sidebar nav */}
      <div
        className="rounded-2xl p-3 shrink-0"
        style={{ width: "220px", background: "#fff", border: "1px solid #f1f5f9", boxShadow: "0 1px 8px rgba(0,0,0,0.04)", height: "fit-content" }}
      >
        {sections.map(({ id, icon: Icon, label }) => (
          <button
            key={id}
            onClick={() => setActiveSection(id)}
            className="w-full flex items-center gap-3 rounded-xl px-3 py-2.5 transition-all text-left"
            style={{
              background: activeSection === id ? "rgba(99,102,241,0.08)" : "transparent",
              color: activeSection === id ? "#6366f1" : "#64748b",
              border: "none",
              cursor: "pointer",
              marginBottom: "2px",
            }}
          >
            <Icon size={15} />
            <span style={{ fontSize: "13px", fontWeight: activeSection === id ? 600 : 500 }}>{label}</span>
            {activeSection === id && <ChevronRight size={13} className="ml-auto" />}
          </button>
        ))}
      </div>

      {/* Content */}
      <div className="flex-1 space-y-5">
        {/* Save notification */}
        {saved && (
          <div
            className="flex items-center gap-2 rounded-xl px-4 py-3"
            style={{ background: "rgba(16,185,129,0.08)", border: "1px solid rgba(16,185,129,0.2)" }}
          >
            <CheckCircle2 size={16} style={{ color: "#10b981" }} />
            <span style={{ fontSize: "13px", color: "#10b981", fontWeight: 500 }}>
              Configuración guardada correctamente
            </span>
          </div>
        )}

        {/* Profile section */}
        {activeSection === "perfil" && (
          <div
            className="rounded-2xl p-5"
            style={{ background: "#fff", border: "1px solid #f1f5f9", boxShadow: "0 1px 8px rgba(0,0,0,0.04)" }}
          >
            <h3 style={{ fontSize: "15px", fontWeight: 600, color: "#0f172a", marginBottom: "20px" }}>
              Perfil de usuario
            </h3>

            {/* Avatar */}
            <div className="flex items-center gap-4 mb-6 pb-5" style={{ borderBottom: "1px solid #f1f5f9" }}>
              <div
                className="rounded-2xl flex items-center justify-center"
                style={{ width: "72px", height: "72px", background: "linear-gradient(135deg, #6366f1, #8b5cf6)" }}
              >
                <span style={{ color: "#fff", fontSize: "24px", fontWeight: 700 }}>JG</span>
              </div>
              <div>
                <button
                  className="rounded-xl px-4 py-2 block mb-2"
                  style={{ background: "rgba(99,102,241,0.08)", color: "#6366f1", border: "none", fontSize: "13px", fontWeight: 600, cursor: "pointer" }}
                >
                  Cambiar foto de perfil
                </button>
                <p style={{ fontSize: "11.5px", color: "#94a3b8" }}>JPG, PNG o GIF. Máximo 5MB</p>
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              {[
                { label: "Nombre completo", field: "nombre", type: "text" },
                { label: "Correo electrónico", field: "email", type: "email" },
                { label: "Teléfono", field: "telefono", type: "text" },
                { label: "Zona horaria", field: "zona", type: "text" },
              ].map(({ label, field, type }) => (
                <div key={field}>
                  <label className="block mb-1.5" style={{ fontSize: "12.5px", fontWeight: 600, color: "#475569" }}>
                    {label}
                  </label>
                  <input
                    type={type}
                    value={profile[field as keyof typeof profile]}
                    onChange={(e) => setProfile((p) => ({ ...p, [field]: e.target.value }))}
                    className="w-full rounded-xl px-4 py-2.5 outline-none"
                    style={{ background: "#f8fafc", border: "1.5px solid #e2e8f0", fontSize: "13.5px", color: "#0f172a" }}
                  />
                </div>
              ))}

              <div>
                <label className="block mb-1.5" style={{ fontSize: "12.5px", fontWeight: 600, color: "#475569" }}>
                  Idioma
                </label>
                <select
                  className="w-full rounded-xl px-4 py-2.5 outline-none"
                  style={{ background: "#f8fafc", border: "1.5px solid #e2e8f0", fontSize: "13.5px", color: "#0f172a" }}
                >
                  <option>Español (México)</option>
                  <option>Español (España)</option>
                  <option>English (US)</option>
                </select>
              </div>
            </div>

            <button
              onClick={handleSave}
              className="mt-5 flex items-center gap-2 rounded-xl px-5 py-2.5"
              style={{ background: "linear-gradient(135deg, #6366f1, #8b5cf6)", color: "#fff", border: "none", fontSize: "13px", fontWeight: 600, cursor: "pointer" }}
            >
              <Save size={14} />
              Guardar cambios
            </button>
          </div>
        )}

        {/* Notifications section */}
        {activeSection === "notificaciones" && (
          <div
            className="rounded-2xl p-5"
            style={{ background: "#fff", border: "1px solid #f1f5f9", boxShadow: "0 1px 8px rgba(0,0,0,0.04)" }}
          >
            <h3 style={{ fontSize: "15px", fontWeight: 600, color: "#0f172a", marginBottom: "20px" }}>
              Preferencias de notificación
            </h3>
            <div className="space-y-4">
              {[
                { key: "newOrder", label: "Nueva orden recibida", desc: "Alerta cuando entra un nuevo pedido" },
                { key: "orderStatus", label: "Cambio de estado de orden", desc: "Cuando se actualiza el estado de un pedido" },
                { key: "whatsappMessages", label: "Mensajes de WhatsApp", desc: "Notificar mensajes sin responder por más de 10 min" },
                { key: "agentAlerts", label: "Alertas del agente IA", desc: "Cuando el agente no puede responder una consulta" },
                { key: "weeklyReport", label: "Reporte semanal", desc: "Resumen de ventas cada lunes por email" },
                { key: "marketingEmails", label: "Emails de marketing", desc: "Novedades, tips y actualizaciones de DropSync" },
                { key: "smsAlerts", label: "Alertas por SMS", desc: "Notificaciones críticas vía mensaje de texto" },
              ].map(({ key, label, desc }) => (
                <div
                  key={key}
                  className="flex items-center justify-between p-4 rounded-xl"
                  style={{ background: "#f8fafc", border: "1px solid #f1f5f9" }}
                >
                  <div>
                    <p style={{ fontSize: "13.5px", fontWeight: 500, color: "#0f172a" }}>{label}</p>
                    <p style={{ fontSize: "12px", color: "#94a3b8", marginTop: "2px" }}>{desc}</p>
                  </div>
                  <Toggle
                    value={notifications[key as keyof typeof notifications]}
                    onChange={() => toggleNotification(key as keyof typeof notifications)}
                  />
                </div>
              ))}
            </div>

            <button
              onClick={handleSave}
              className="mt-5 flex items-center gap-2 rounded-xl px-5 py-2.5"
              style={{ background: "linear-gradient(135deg, #6366f1, #8b5cf6)", color: "#fff", border: "none", fontSize: "13px", fontWeight: 600, cursor: "pointer" }}
            >
              <Save size={14} />
              Guardar preferencias
            </button>
          </div>
        )}

        {/* Security section */}
        {activeSection === "seguridad" && (
          <div className="space-y-4">
            <div
              className="rounded-2xl p-5"
              style={{ background: "#fff", border: "1px solid #f1f5f9", boxShadow: "0 1px 8px rgba(0,0,0,0.04)" }}
            >
              <h3 style={{ fontSize: "15px", fontWeight: 600, color: "#0f172a", marginBottom: "20px" }}>
                Cambiar contraseña
              </h3>
              <div className="space-y-4 max-w-sm">
                <div>
                  <label className="block mb-1.5" style={{ fontSize: "12.5px", fontWeight: 600, color: "#475569" }}>
                    Contraseña actual
                  </label>
                  <div className="relative">
                    <input
                      type={showCurrentPw ? "text" : "password"}
                      className="w-full rounded-xl px-4 py-2.5 outline-none pr-12"
                      placeholder="••••••••"
                      style={{ background: "#f8fafc", border: "1.5px solid #e2e8f0", fontSize: "13.5px" }}
                    />
                    <button className="absolute right-4 top-1/2 -translate-y-1/2" onClick={() => setShowCurrentPw(!showCurrentPw)} style={{ border: "none", background: "transparent", color: "#94a3b8", cursor: "pointer" }}>
                      {showCurrentPw ? <EyeOff size={15} /> : <Eye size={15} />}
                    </button>
                  </div>
                </div>
                <div>
                  <label className="block mb-1.5" style={{ fontSize: "12.5px", fontWeight: 600, color: "#475569" }}>
                    Nueva contraseña
                  </label>
                  <div className="relative">
                    <input
                      type={showNewPw ? "text" : "password"}
                      className="w-full rounded-xl px-4 py-2.5 outline-none pr-12"
                      placeholder="Mínimo 8 caracteres"
                      style={{ background: "#f8fafc", border: "1.5px solid #e2e8f0", fontSize: "13.5px" }}
                    />
                    <button className="absolute right-4 top-1/2 -translate-y-1/2" onClick={() => setShowNewPw(!showNewPw)} style={{ border: "none", background: "transparent", color: "#94a3b8", cursor: "pointer" }}>
                      {showNewPw ? <EyeOff size={15} /> : <Eye size={15} />}
                    </button>
                  </div>
                </div>
                <div>
                  <label className="block mb-1.5" style={{ fontSize: "12.5px", fontWeight: 600, color: "#475569" }}>
                    Confirmar nueva contraseña
                  </label>
                  <input
                    type="password"
                    className="w-full rounded-xl px-4 py-2.5 outline-none"
                    placeholder="••••••••"
                    style={{ background: "#f8fafc", border: "1.5px solid #e2e8f0", fontSize: "13.5px" }}
                  />
                </div>
                <button
                  onClick={handleSave}
                  className="flex items-center gap-2 rounded-xl px-5 py-2.5"
                  style={{ background: "linear-gradient(135deg, #6366f1, #8b5cf6)", color: "#fff", border: "none", fontSize: "13px", fontWeight: 600, cursor: "pointer" }}
                >
                  <Key size={14} />
                  Actualizar contraseña
                </button>
              </div>
            </div>

            <div
              className="rounded-2xl p-5"
              style={{ background: "#fff", border: "1px solid #f1f5f9", boxShadow: "0 1px 8px rgba(0,0,0,0.04)" }}
            >
              <div className="flex items-center justify-between">
                <div>
                  <h4 style={{ fontSize: "14px", fontWeight: 600, color: "#0f172a" }}>
                    Autenticación de dos factores (2FA)
                  </h4>
                  <p style={{ fontSize: "12.5px", color: "#94a3b8", marginTop: "4px" }}>
                    Agrega una capa extra de seguridad a tu cuenta
                  </p>
                </div>
                <button
                  className="rounded-xl px-4 py-2"
                  style={{ background: "rgba(99,102,241,0.08)", color: "#6366f1", border: "none", fontSize: "13px", fontWeight: 600, cursor: "pointer" }}
                >
                  Activar 2FA
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Subscription section */}
        {activeSection === "suscripcion" && (
          <div className="space-y-4">
            {/* Current plan */}
            <div
              className="rounded-2xl p-5"
              style={{
                background: "linear-gradient(135deg, rgba(99,102,241,0.06), rgba(139,92,246,0.04))",
                border: "1.5px solid rgba(99,102,241,0.2)",
                boxShadow: "0 1px 8px rgba(0,0,0,0.04)",
              }}
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div
                    className="rounded-xl flex items-center justify-center"
                    style={{ width: "44px", height: "44px", background: "linear-gradient(135deg, #6366f1, #8b5cf6)" }}
                  >
                    <Zap size={20} style={{ color: "#fff" }} />
                  </div>
                  <div>
                    <p style={{ fontSize: "16px", fontWeight: 700, color: "#6366f1" }}>Plan Pro</p>
                    <p style={{ fontSize: "13px", color: "#94a3b8" }}>$899 MXN/mes · Renovación: 13 May 2026</p>
                  </div>
                </div>
                <button
                  className="rounded-xl px-4 py-2"
                  style={{ background: "#6366f1", color: "#fff", border: "none", fontSize: "13px", fontWeight: 600, cursor: "pointer" }}
                >
                  Cambiar plan
                </button>
              </div>

              <div className="grid grid-cols-3 gap-3 mt-5">
                {[
                  { label: "Productos", value: "Ilimitados", used: "1,248 usados" },
                  { label: "WhatsApp API", value: "Incluido", used: "Activo" },
                  { label: "Agente IA", value: "Incluido", used: "89 conv. hoy" },
                ].map(({ label, value, used }) => (
                  <div key={label} className="rounded-xl p-3" style={{ background: "rgba(255,255,255,0.6)", border: "1px solid rgba(99,102,241,0.1)" }}>
                    <p style={{ fontSize: "13.5px", fontWeight: 700, color: "#6366f1" }}>{value}</p>
                    <p style={{ fontSize: "11.5px", color: "#0f172a", fontWeight: 500 }}>{label}</p>
                    <p style={{ fontSize: "11px", color: "#94a3b8", marginTop: "2px" }}>{used}</p>
                  </div>
                ))}
              </div>
            </div>

            {/* Payment method */}
            <div
              className="rounded-2xl p-5"
              style={{ background: "#fff", border: "1px solid #f1f5f9", boxShadow: "0 1px 8px rgba(0,0,0,0.04)" }}
            >
              <h3 style={{ fontSize: "14px", fontWeight: 600, color: "#0f172a", marginBottom: "16px" }}>
                Método de pago
              </h3>
              <div className="flex items-center gap-3 rounded-xl p-4" style={{ background: "#f8fafc", border: "1px solid #e2e8f0" }}>
                <div
                  className="rounded-lg flex items-center justify-center"
                  style={{ width: "44px", height: "28px", background: "#1a1f71" }}
                >
                  <span style={{ color: "#fff", fontSize: "10px", fontWeight: 900 }}>VISA</span>
                </div>
                <div className="flex-1">
                  <p style={{ fontSize: "13.5px", fontWeight: 500, color: "#0f172a" }}>
                    •••• •••• •••• 4821
                  </p>
                  <p style={{ fontSize: "11.5px", color: "#94a3b8" }}>Vence 09/27</p>
                </div>
                <button style={{ background: "none", border: "none", color: "#6366f1", fontSize: "12.5px", fontWeight: 600, cursor: "pointer" }}>
                  Cambiar
                </button>
              </div>
            </div>

            {/* Billing history */}
            <div
              className="rounded-2xl p-5"
              style={{ background: "#fff", border: "1px solid #f1f5f9", boxShadow: "0 1px 8px rgba(0,0,0,0.04)" }}
            >
              <h3 style={{ fontSize: "14px", fontWeight: 600, color: "#0f172a", marginBottom: "16px" }}>
                Historial de facturación
              </h3>
              <div className="space-y-2">
                {[
                  { date: "13 Abr 2026", amount: "$899", status: "Pagado" },
                  { date: "13 Mar 2026", amount: "$899", status: "Pagado" },
                  { date: "13 Feb 2026", amount: "$899", status: "Pagado" },
                ].map((invoice) => (
                  <div
                    key={invoice.date}
                    className="flex items-center justify-between p-3 rounded-xl"
                    style={{ background: "#f8fafc" }}
                  >
                    <span style={{ fontSize: "13px", color: "#374151" }}>{invoice.date}</span>
                    <span style={{ fontSize: "13.5px", fontWeight: 600, color: "#0f172a" }}>
                      {invoice.amount} MXN
                    </span>
                    <div className="flex items-center gap-2">
                      <div
                        className="flex items-center gap-1.5 rounded-full px-2.5 py-0.5"
                        style={{ background: "rgba(16,185,129,0.1)", color: "#10b981" }}
                      >
                        <CheckCircle2 size={11} />
                        <span style={{ fontSize: "11px", fontWeight: 600 }}>{invoice.status}</span>
                      </div>
                      <button style={{ background: "none", border: "none", color: "#94a3b8", cursor: "pointer", fontSize: "12px" }}>
                        PDF
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Appearance section */}
        {activeSection === "apariencia" && (
          <div
            className="rounded-2xl p-5"
            style={{ background: "#fff", border: "1px solid #f1f5f9", boxShadow: "0 1px 8px rgba(0,0,0,0.04)" }}
          >
            <h3 style={{ fontSize: "15px", fontWeight: 600, color: "#0f172a", marginBottom: "20px" }}>
              Apariencia y tema
            </h3>
            <div className="space-y-5">
              <div>
                <p style={{ fontSize: "13px", fontWeight: 600, color: "#374151", marginBottom: "12px" }}>Tema del panel</p>
                <div className="grid grid-cols-3 gap-3">
                  {[
                    { id: "light", label: "Claro", preview: ["#fff", "#f8fafc", "#0f172a"] },
                    { id: "dark", label: "Oscuro", preview: ["#0f172a", "#1e293b", "#e2e8f0"] },
                    { id: "auto", label: "Automático", preview: ["#f8fafc", "#0f172a", "#6366f1"] },
                  ].map(({ id, label, preview }) => (
                    <button
                      key={id}
                      className="rounded-xl p-3 text-left transition-all"
                      style={{
                        background: id === "light" ? "rgba(99,102,241,0.06)" : "#f8fafc",
                        border: id === "light" ? "1.5px solid #6366f1" : "1.5px solid #e2e8f0",
                        cursor: "pointer",
                      }}
                    >
                      <div className="flex gap-1 mb-3">
                        {preview.map((color, i) => (
                          <div key={i} className="rounded-md flex-1 h-8" style={{ background: color }} />
                        ))}
                      </div>
                      <p style={{ fontSize: "12.5px", fontWeight: 600, color: "#374151" }}>{label}</p>
                    </button>
                  ))}
                </div>
              </div>

              <div>
                <p style={{ fontSize: "13px", fontWeight: 600, color: "#374151", marginBottom: "12px" }}>Color de acento</p>
                <div className="flex gap-3">
                  {[
                    "#6366f1", "#8b5cf6", "#3b82f6", "#10b981", "#f59e0b", "#ef4444", "#ec4899",
                  ].map((color) => (
                    <button
                      key={color}
                      className="rounded-full transition-all"
                      style={{
                        width: "32px",
                        height: "32px",
                        background: color,
                        border: color === "#6366f1" ? "3px solid #0f172a" : "3px solid transparent",
                        cursor: "pointer",
                      }}
                    />
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Integrations section */}
        {activeSection === "integraciones" && (
          <div className="space-y-4">
            {[
              {
                name: "Shopify",
                desc: "Sincroniza productos e inventario con tu tienda Shopify",
                logo: "🛍️",
                connected: true,
              },
              {
                name: "WooCommerce",
                desc: "Integra con tu sitio WordPress/WooCommerce",
                logo: "🌐",
                connected: false,
              },
              {
                name: "MercadoLibre",
                desc: "Publica y gestiona tus productos en MercadoLibre",
                logo: "🟡",
                connected: false,
              },
              {
                name: "Google Sheets",
                desc: "Sincroniza catálogos y reportes con Google Sheets",
                logo: "📊",
                connected: true,
              },
              {
                name: "Mailchimp",
                desc: "Envía campañas de email marketing a tus clientes",
                logo: "📧",
                connected: false,
              },
            ].map((integration) => (
              <div
                key={integration.name}
                className="rounded-2xl p-5 flex items-center gap-4"
                style={{ background: "#fff", border: "1px solid #f1f5f9", boxShadow: "0 1px 8px rgba(0,0,0,0.04)" }}
              >
                <div
                  className="rounded-xl flex items-center justify-center text-2xl shrink-0"
                  style={{ width: "48px", height: "48px", background: "#f8fafc", border: "1px solid #f1f5f9" }}
                >
                  {integration.logo}
                </div>
                <div className="flex-1">
                  <div className="flex items-center gap-2">
                    <p style={{ fontSize: "14px", fontWeight: 600, color: "#0f172a" }}>{integration.name}</p>
                    {integration.connected && (
                      <div
                        className="flex items-center gap-1 rounded-full px-2 py-0.5"
                        style={{ background: "rgba(16,185,129,0.1)", color: "#10b981" }}
                      >
                        <CheckCircle2 size={11} />
                        <span style={{ fontSize: "10.5px", fontWeight: 600 }}>Conectado</span>
                      </div>
                    )}
                  </div>
                  <p style={{ fontSize: "12.5px", color: "#94a3b8", marginTop: "2px" }}>{integration.desc}</p>
                </div>
                <button
                  className="rounded-xl px-4 py-2"
                  style={{
                    background: integration.connected ? "#f8fafc" : "rgba(99,102,241,0.08)",
                    color: integration.connected ? "#64748b" : "#6366f1",
                    border: integration.connected ? "1px solid #e2e8f0" : "none",
                    fontSize: "12.5px",
                    fontWeight: 600,
                    cursor: "pointer",
                  }}
                >
                  {integration.connected ? "Desconectar" : "Conectar"}
                </button>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
