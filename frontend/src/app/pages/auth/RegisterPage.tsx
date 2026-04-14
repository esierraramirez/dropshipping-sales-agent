import { useState } from "react";
import { Link, useNavigate } from "react-router";
import { Eye, EyeOff, Zap, ArrowRight, CheckCircle2 } from "lucide-react";
import { api, ApiError, type AuthResponse } from "../../lib/api";
import { setAuthState } from "../../lib/auth";

export function RegisterPage() {
  const navigate = useNavigate();
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [form, setForm] = useState({
    name: "",
    email: "",
    password: "",
    rfc: "",
    sector: "",
    country: "México",
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const response = await api.post<AuthResponse>(
        "/auth/register",
        {
          name: form.name,
          email: form.email,
          password: form.password,
          rfc: form.rfc || undefined,
          sector: form.sector || undefined,
          country: form.country,
        },
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
        setError("No fue posible crear la cuenta. Revisa la conexión con el backend.");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center px-4 py-12" style={{ background: "#f8fafc" }}>
      <div className="w-full max-w-md">
        {/* Logo */}
        <div className="flex items-center justify-center gap-3 mb-8">
          <div
            className="flex items-center justify-center rounded-xl"
            style={{ width: "42px", height: "42px", background: "linear-gradient(135deg, #6366f1, #8b5cf6)" }}
          >
            <Zap size={20} color="#fff" />
          </div>
          <span style={{ fontSize: "22px", fontWeight: 700, color: "#0f172a", letterSpacing: "-0.5px" }}>
            DropSync
          </span>
        </div>

        <div
          className="rounded-2xl p-8"
          style={{ background: "#fff", border: "1px solid #e2e8f0", boxShadow: "0 4px 24px rgba(0,0,0,0.06)" }}
        >
          <div className="mb-7">
            <h2 style={{ fontSize: "22px", fontWeight: 700, color: "#0f172a" }}>
              Crea tu cuenta
            </h2>
            <p style={{ color: "#94a3b8", fontSize: "13.5px", marginTop: "4px" }}>
              Comienza tu prueba gratuita de 14 días
            </p>
          </div>

          {/* Benefits */}
          <div className="flex gap-4 mb-6 flex-wrap">
            {["Sin tarjeta de crédito", "Cancelar cuando quieras", "Soporte 24/7"].map((b) => (
              <div key={b} className="flex items-center gap-1.5">
                <CheckCircle2 size={13} style={{ color: "#10b981" }} />
                <span style={{ fontSize: "11.5px", color: "#64748b" }}>{b}</span>
              </div>
            ))}
          </div>

          <form onSubmit={handleRegister} className="space-y-4">
            <div>
              <label className="block mb-1.5" style={{ fontSize: "13px", fontWeight: 600, color: "#374151" }}>
                Nombre de empresa
              </label>
              <input
                type="text"
                name="name"
                value={form.name}
                onChange={handleChange}
                className="w-full rounded-xl px-4 py-3 outline-none"
                style={{ background: "#f8fafc", border: "1.5px solid #e2e8f0", fontSize: "14px", color: "#0f172a" }}
                placeholder="Mi Tienda Online"
                required
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block mb-1.5" style={{ fontSize: "13px", fontWeight: 600, color: "#374151" }}>
                  RFC (opcional)
                </label>
                <input
                  type="text"
                  name="rfc"
                  value={form.rfc}
                  onChange={handleChange}
                  className="w-full rounded-xl px-4 py-3 outline-none"
                  style={{ background: "#f8fafc", border: "1.5px solid #e2e8f0", fontSize: "14px", color: "#0f172a" }}
                  placeholder="ABC123456XYZ"
                />
              </div>
              <div>
                <label className="block mb-1.5" style={{ fontSize: "13px", fontWeight: 600, color: "#374151" }}>
                  Sector (opcional)
                </label>
                <input
                  type="text"
                  name="sector"
                  value={form.sector}
                  onChange={handleChange}
                  className="w-full rounded-xl px-4 py-3 outline-none"
                  style={{ background: "#f8fafc", border: "1.5px solid #e2e8f0", fontSize: "14px", color: "#0f172a" }}
                  placeholder="Moda, Electrónica, etc."
                />
              </div>
            </div>

            <div>
              <label className="block mb-1.5" style={{ fontSize: "13px", fontWeight: 600, color: "#374151" }}>
                Correo electrónico
              </label>
              <input
                type="email"
                name="email"
                value={form.email}
                onChange={handleChange}
                className="w-full rounded-xl px-4 py-3 outline-none"
                style={{ background: "#f8fafc", border: "1.5px solid #e2e8f0", fontSize: "14px", color: "#0f172a" }}
                placeholder="tu@empresa.com"
                required
              />
            </div>

            <div>
              <label className="block mb-1.5" style={{ fontSize: "13px", fontWeight: 600, color: "#374151" }}>
                Contraseña
              </label>
              <div className="relative">
                <input
                  type={showPassword ? "text" : "password"}
                  name="password"
                  value={form.password}
                  onChange={handleChange}
                  className="w-full rounded-xl px-4 py-3 outline-none pr-12"
                  style={{ background: "#f8fafc", border: "1.5px solid #e2e8f0", fontSize: "14px", color: "#0f172a" }}
                  placeholder="Mínimo 8 caracteres"
                  required
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

            <div>
              <label className="block mb-1.5" style={{ fontSize: "13px", fontWeight: 600, color: "#374151" }}>
                País / Región
              </label>
              <select
                name="country"
                value={form.country}
                onChange={handleChange}
                className="w-full rounded-xl px-4 py-3 outline-none"
                style={{ background: "#f8fafc", border: "1.5px solid #e2e8f0", fontSize: "14px", color: "#0f172a" }}
              >
                <option>México</option>
                <option>Colombia</option>
                <option>Argentina</option>
                <option>España</option>
                <option>Perú</option>
                <option>Chile</option>
              </select>
            </div>
                  Nombre completo
                </label>
                <input
                  type="text"
                  name="name"
                  value={form.name}
                  onChange={handleChange}
                  className="w-full rounded-xl px-4 py-3 outline-none"
                  style={{ background: "#f8fafc", border: "1.5px solid #e2e8f0", fontSize: "14px", color: "#0f172a" }}
                  placeholder="Juan García"
                />
              </div>
              <div>
                <label className="block mb-1.5" style={{ fontSize: "13px", fontWeight: 600, color: "#374151" }}>
                  Nombre de empresa
                </label>
                <input
                  type="text"
                  name="empresa"
                  value={form.empresa}
                  onChange={handleChange}
                  className="w-full rounded-xl px-4 py-3 outline-none"
                  style={{ background: "#f8fafc", border: "1.5px solid #e2e8f0", fontSize: "14px", color: "#0f172a" }}
                  placeholder="Mi Tienda Online"
                />
              </div>
            </div>

            <div>
              <label className="block mb-1.5" style={{ fontSize: "13px", fontWeight: 600, color: "#374151" }}>
                Correo electrónico
              </label>
              <input
                type="email"
                name="email"
                value={form.email}
                onChange={handleChange}
                className="w-full rounded-xl px-4 py-3 outline-none"
                style={{ background: "#f8fafc", border: "1.5px solid #e2e8f0", fontSize: "14px", color: "#0f172a" }}
                placeholder="tu@empresa.com"
              />
            </div>

            <div>
              <label className="block mb-1.5" style={{ fontSize: "13px", fontWeight: 600, color: "#374151" }}>
                Contraseña
              </label>
              <div className="relative">
                <input
                  type={showPassword ? "text" : "password"}
                  name="password"
                  value={form.password}
                  onChange={handleChange}
                  className="w-full rounded-xl px-4 py-3 outline-none pr-12"
                  style={{ background: "#f8fafc", border: "1.5px solid #e2e8f0", fontSize: "14px", color: "#0f172a" }}
                  placeholder="Mínimo 8 caracteres"
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

            <div>
              <label className="block mb-1.5" style={{ fontSize: "13px", fontWeight: 600, color: "#374151" }}>
                País / Región
              </label>
              <select
                className="w-full rounded-xl px-4 py-3 outline-none"
                style={{ background: "#f8fafc", border: "1.5px solid #e2e8f0", fontSize: "14px", color: "#0f172a" }}
              >
                <option>México</option>
                <option>Colombia</option>
                <option>Argentina</option>
                <option>España</option>
                <option>Perú</option>
                <option>Chile</option>
              </select>
            </div>

            <div className="flex items-start gap-3">
              <input type="checkbox" id="terms" className="mt-1" />
              <label htmlFor="terms" style={{ fontSize: "12.5px", color: "#64748b", fontWeight: 400 }}>
                Acepto los{" "}
                <a href="#" style={{ color: "#6366f1" }}>Términos de servicio</a>
                {" "}y la{" "}
                <a href="#" style={{ color: "#6366f1" }}>Política de privacidad</a>
              </label>
            </div>

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
                background: loading ? "#c7d2fe" : "linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)",
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
                  Creando cuenta...
                </>
              ) : (
                <>
                  Crear cuenta gratis
                  <ArrowRight size={16} />
                </>
              )}
            </button>
          </form>

          <p className="text-center mt-5" style={{ fontSize: "13.5px", color: "#94a3b8" }}>
            ¿Ya tienes cuenta?{" "}
            <Link to="/login" style={{ color: "#6366f1", fontWeight: 600 }}>
              Iniciar sesión
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}
