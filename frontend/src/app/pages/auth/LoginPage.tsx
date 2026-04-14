import { useState } from "react";
import { Link, useNavigate } from "react-router";
import { Eye, EyeOff, Zap, ArrowRight, Package, Bot, MessageCircle } from "lucide-react";
import { api, ApiError, type AuthResponse } from "../../lib/api";
import { setAuthState } from "../../lib/auth";

export function LoginPage() {
  const navigate = useNavigate();
  const [showPassword, setShowPassword] = useState(false);
  const [email, setEmail] = useState("demo@dropsync.io");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const response = await api.post<AuthResponse>(
        "/auth/login",
        { email, password },
        false
      );

      setAuthState({
        accessToken: response.access_token,
        tokenType: response.token_type,
        vendor: response.vendor,
      });

      navigate("/dashboard");
    } catch (err) {
      if (err instanceof ApiError) {
        setError(err.detail);
      } else {
        setError("No fue posible iniciar sesión. Revisa la conexión con el backend.");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex" style={{ background: "#f8fafc" }}>
      {/* Left Panel */}
      <div
        className="hidden lg:flex flex-col justify-between p-12 flex-1"
        style={{ background: "linear-gradient(135deg, #0f172a 0%, #1e293b 60%, #312e81 100%)" }}
      >
        {/* Logo */}
        <div className="flex items-center gap-3">
          <div
            className="flex items-center justify-center rounded-xl"
            style={{
              width: "42px",
              height: "42px",
              background: "linear-gradient(135deg, #6366f1, #8b5cf6)",
            }}
          >
            <Zap size={20} color="#fff" />
          </div>
          <span style={{ color: "#fff", fontSize: "20px", fontWeight: 700, letterSpacing: "-0.5px" }}>
            DropSync
          </span>
        </div>

        {/* Center content */}
        <div>
          <div className="mb-10">
            <h2
              style={{
                fontSize: "38px",
                fontWeight: 700,
                color: "#fff",
                lineHeight: 1.2,
                letterSpacing: "-1px",
                marginBottom: "16px",
              }}
            >
              Gestiona tu dropshipping
              <br />
              <span style={{ color: "#a5b4fc" }}>de forma inteligente</span>
            </h2>
            <p style={{ color: "#94a3b8", fontSize: "16px", lineHeight: 1.7 }}>
              Automatiza tu negocio con IA, gestiona catálogos y conecta WhatsApp Business desde una sola plataforma.
            </p>
          </div>

          {/* Features */}
          <div className="space-y-4">
            {[
              { icon: Package, label: "Catálogo sincronizado", desc: "Sube y gestiona productos con Excel" },
              { icon: Bot, label: "Agente IA 24/7", desc: "Responde automáticamente a tus clientes" },
              { icon: MessageCircle, label: "WhatsApp Business", desc: "Conecta tu número oficial en minutos" },
            ].map(({ icon: Icon, label, desc }) => (
              <div key={label} className="flex items-center gap-4">
                <div
                  className="flex items-center justify-center rounded-lg shrink-0"
                  style={{
                    width: "40px",
                    height: "40px",
                    background: "rgba(99,102,241,0.15)",
                    border: "1px solid rgba(99,102,241,0.3)",
                  }}
                >
                  <Icon size={18} style={{ color: "#a5b4fc" }} />
                </div>
                <div>
                  <p style={{ color: "#e2e8f0", fontSize: "14px", fontWeight: 600 }}>{label}</p>
                  <p style={{ color: "#64748b", fontSize: "12.5px" }}>{desc}</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Testimonial */}
        <div
          className="rounded-2xl p-5"
          style={{ background: "rgba(255,255,255,0.05)", border: "1px solid rgba(255,255,255,0.08)" }}
        >
          <p style={{ color: "#cbd5e1", fontSize: "14px", lineHeight: 1.7, fontStyle: "italic" }}>
            "DropSync transformó la forma en que gestionamos nuestras ventas. Las órdenes se procesan solas y el agente IA atiende a los clientes a cualquier hora."
          </p>
          <div className="flex items-center gap-3 mt-4">
            <div
              className="rounded-full flex items-center justify-center"
              style={{ width: "36px", height: "36px", background: "linear-gradient(135deg, #f59e0b, #ef4444)" }}
            >
              <span style={{ color: "#fff", fontSize: "13px", fontWeight: 700 }}>ML</span>
            </div>
            <div>
              <p style={{ color: "#e2e8f0", fontSize: "13px", fontWeight: 600 }}>María López</p>
              <p style={{ color: "#64748b", fontSize: "12px" }}>CEO, Moda Express MX</p>
            </div>
          </div>
        </div>
      </div>

      {/* Right Panel - Login Form */}
      <div className="flex flex-col justify-center items-center flex-1 px-8 lg:max-w-md w-full">
        {/* Mobile logo */}
        <div className="lg:hidden flex items-center gap-3 mb-10">
          <div
            className="flex items-center justify-center rounded-xl"
            style={{ width: "40px", height: "40px", background: "linear-gradient(135deg, #6366f1, #8b5cf6)" }}
          >
            <Zap size={18} color="#fff" />
          </div>
          <span style={{ fontSize: "20px", fontWeight: 700, color: "#0f172a" }}>DropSync</span>
        </div>

        <div className="w-full max-w-sm">
          <div className="mb-8">
            <h2 style={{ fontSize: "26px", fontWeight: 700, color: "#0f172a", letterSpacing: "-0.5px" }}>
              Bienvenido de vuelta
            </h2>
            <p style={{ color: "#94a3b8", fontSize: "14px", marginTop: "6px" }}>
              Inicia sesión en tu cuenta de DropSync
            </p>
          </div>

          {/* Demo badge */}
          <div
            className="flex items-center gap-2 rounded-xl px-4 py-3 mb-6"
            style={{ background: "rgba(99,102,241,0.08)", border: "1px solid rgba(99,102,241,0.2)" }}
          >
            <Zap size={14} style={{ color: "#6366f1" }} />
            <span style={{ fontSize: "12.5px", color: "#6366f1", fontWeight: 500 }}>
              Modo demo activo — haz clic en Iniciar sesión
            </span>
          </div>

          <form onSubmit={handleLogin} className="space-y-4">
            {/* Email */}
            <div>
              <label
                className="block mb-1.5"
                style={{ fontSize: "13px", fontWeight: 600, color: "#374151" }}
              >
                Correo electrónico
              </label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full rounded-xl px-4 py-3 outline-none transition-all"
                style={{
                  background: "#f8fafc",
                  border: "1.5px solid #e2e8f0",
                  fontSize: "14px",
                  color: "#0f172a",
                }}
                placeholder="tu@empresa.com"
              />
            </div>

            {/* Password */}
            <div>
              <label
                className="block mb-1.5"
                style={{ fontSize: "13px", fontWeight: 600, color: "#374151" }}
              >
                Contraseña
              </label>
              <div className="relative">
                <input
                  type={showPassword ? "text" : "password"}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="w-full rounded-xl px-4 py-3 outline-none transition-all pr-12"
                  style={{
                    background: "#f8fafc",
                    border: "1.5px solid #e2e8f0",
                    fontSize: "14px",
                    color: "#0f172a",
                  }}
                  placeholder="••••••••"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-4 top-1/2 -translate-y-1/2"
                  style={{ color: "#94a3b8" }}
                >
                  {showPassword ? <EyeOff size={16} /> : <Eye size={16} />}
                </button>
              </div>
            </div>

            {/* Forgot password */}
            <div className="flex justify-end">
              <a href="#" style={{ fontSize: "13px", color: "#6366f1", fontWeight: 500 }}>
                ¿Olvidaste tu contraseña?
              </a>
            </div>

            {/* Submit */}
            {error && (
              <div
                className="rounded-xl px-3 py-2"
                style={{ background: "rgba(239,68,68,0.08)", border: "1px solid rgba(239,68,68,0.25)" }}
              >
                <p style={{ fontSize: "12.5px", color: "#b91c1c", fontWeight: 500 }}>{error}</p>
              </div>
            )}

            <button
              type="submit"
              disabled={loading}
              className="w-full flex items-center justify-center gap-2 rounded-xl py-3 transition-all"
              style={{
                background: loading
                  ? "#c7d2fe"
                  : "linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)",
                color: "#fff",
                fontSize: "14px",
                fontWeight: 600,
                border: "none",
                cursor: loading ? "not-allowed" : "pointer",
              }}
            >
              {loading ? (
                <>
                  <div
                    className="rounded-full border-2 border-white/30 border-t-white animate-spin"
                    style={{ width: "16px", height: "16px" }}
                  />
                  Iniciando sesión...
                </>
              ) : (
                <>
                  Iniciar sesión
                  <ArrowRight size={16} />
                </>
              )}
            </button>
          </form>

          <p className="text-center mt-6" style={{ fontSize: "13.5px", color: "#94a3b8" }}>
            ¿No tienes cuenta?{" "}
            <Link to="/register" style={{ color: "#6366f1", fontWeight: 600 }}>
              Regístrate gratis
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}
