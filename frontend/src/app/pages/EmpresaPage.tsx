import { useEffect, useState } from "react";
import { Building2, MapPin, Phone, Globe, Mail, Camera, Save, Edit3, CheckCircle2 } from "lucide-react";
import { api, ApiError } from "../lib/api";

interface VendorData {
  id: number;
  name: string;
  email: string;
  rfc: string | null;
  sector: string | null;
  phone: string | null;
  website: string | null;
  address: string | null;
  city: string | null;
  state: string | null;
  country: string | null;
  postal_code: string | null;
  description: string | null;
}

interface Stats {
  total_products: number;
  total_orders: number;
  total_customers: number;
}

function FormField({
  label,
  value,
  onChange,
  type = "text",
  placeholder,
  editing,
}: {
  label: string;
  value: string | null;
  onChange: (v: string) => void;
  type?: string;
  placeholder?: string;
  editing: boolean;
}) {
  return (
    <div>
      <label className="block mb-1.5" style={{ fontSize: "12.5px", fontWeight: 600, color: "#475569" }}>
        {label}
      </label>
      {editing ? (
        <input
          type={type}
          value={value || ""}
          onChange={(e) => onChange(e.target.value)}
          placeholder={placeholder}
          className="w-full rounded-xl px-4 py-2.5 outline-none transition-all"
          style={{
            background: "#f8fafc",
            border: "1.5px solid #6366f1",
            fontSize: "13.5px",
            color: "#0f172a",
          }}
        />
      ) : (
        <div
          className="rounded-xl px-4 py-2.5"
          style={{ background: "#f8fafc", border: "1px solid #f1f5f9", fontSize: "13.5px", color: "#0f172a" }}
        >
          {value || <span style={{ color: "#cbd5e1" }}>—</span>}
        </div>
      )}
    </div>
  );
}

export function EmpresaPage() {
  const [vendor, setVendor] = useState<VendorData | null>(null);
  const [stats, setStats] = useState<Stats | null>(null);
  const [editing, setEditing] = useState(false);
  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  const [editData, setEditData] = useState<Partial<VendorData>>({});

  // Cargar datos al montar
  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      setError("");
      const [vendorRes, statsRes] = await Promise.all([
        api.get<VendorData>("/empresa/me", true),
        api.get<Stats>("/empresa/me/stats", true),
      ]);
      setVendor(vendorRes);
      setStats(statsRes);
      setEditData(vendorRes);
    } catch (err) {
      console.error("Error cargando datos:", err);
      setError("No se pudieron cargar los datos de la empresa");
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async () => {
    if (!vendor) return;
    try {
      setSaving(true);
      setError("");
      const updated = await api.patch<VendorData>("/empresa/me", editData, true);
      setVendor(updated);
      setEditData(updated);
      setEditing(false);
      setSaved(true);
      setTimeout(() => setSaved(false), 3000);
    } catch (err) {
      if (err instanceof ApiError) {
        setError(err.detail);
      } else {
        setError("Error al guardar cambios");
      }
    } finally {
      setSaving(false);
    }
  };

  const updateEditField = <K extends keyof VendorData>(key: K, value: any) => {
    setEditData((prev) => ({ ...prev, [key]: value || null }));
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div style={{ textAlign: "center" }}>
          <div style={{ fontSize: "32px", marginBottom: "10px" }}>🏢</div>
          <p style={{ color: "#64748b", marginBottom: "4px" }}>Cargando información...</p>
        </div>
      </div>
    );
  }

  if (!vendor) {
    return (
      <div className="flex items-center justify-center h-96">
        <div style={{ textAlign: "center" }}>
          <div style={{ fontSize: "32px", marginBottom: "10px" }}>⚠️</div>
          <p style={{ color: "#ef4444" }}>{error || "No se pudo cargar la información"}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto space-y-5">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div />
        <div className="flex items-center gap-3">
          {saved && (
            <div className="flex items-center gap-2 rounded-xl px-4 py-2"
              style={{ background: "rgba(16,185,129,0.1)", border: "1px solid rgba(16,185,129,0.2)" }}
            >
              <CheckCircle2 size={14} style={{ color: "#10b981" }} />
              <span style={{ fontSize: "13px", color: "#10b981", fontWeight: 500 }}>Cambios guardados</span>
            </div>
          )}
          {error && (
            <div className="flex items-center gap-2 rounded-xl px-4 py-2"
              style={{ background: "rgba(239,68,68,0.1)", border: "1px solid rgba(239,68,68,0.2)" }}
            >
              <span style={{ fontSize: "13px", color: "#ef4444", fontWeight: 500 }}>{error}</span>
            </div>
          )}
          {editing ? (
            <button
              onClick={handleSave}
              disabled={saving}
              className="flex items-center gap-2 rounded-xl px-5 py-2.5"
              style={{ background: "linear-gradient(135deg, #6366f1, #8b5cf6)", color: "#fff", fontSize: "13px", fontWeight: 600, border: "none", cursor: saving ? "wait" : "pointer", opacity: saving ? 0.7 : 1 }}
            >
              <Save size={14} />
              {saving ? "Guardando..." : "Guardar cambios"}
            </button>
          ) : (
            <button
              onClick={() => setEditing(true)}
              className="flex items-center gap-2 rounded-xl px-5 py-2.5"
              style={{ background: "#f8fafc", border: "1.5px solid #e2e8f0", color: "#374151", fontSize: "13px", fontWeight: 600, cursor: "pointer" }}
            >
              <Edit3 size={14} />
              Editar información
            </button>
          )}
        </div>
      </div>

      {/* Profile card */}
      <div
        className="rounded-2xl p-6"
        style={{ background: "#fff", border: "1px solid #f1f5f9", boxShadow: "0 1px 8px rgba(0,0,0,0.04)" }}
      >
        <div className="flex items-center gap-5">
          <div className="relative">
            <div
              className="rounded-2xl flex items-center justify-center"
              style={{
                width: "80px",
                height: "80px",
                background: "linear-gradient(135deg, #6366f1, #8b5cf6)",
              }}
            >
              <Building2 size={32} style={{ color: "#fff" }} />
            </div>
          </div>
          <div>
            <h2 style={{ fontSize: "20px", fontWeight: 700, color: "#0f172a" }}>{vendor.name}</h2>
            <p style={{ fontSize: "13px", color: "#94a3b8", marginTop: "2px" }}>{vendor.sector || "Sector no especificado"}</p>
            <div className="flex items-center gap-4 mt-3">
              <div className="flex items-center gap-1.5">
                <div className="rounded-full" style={{ width: "8px", height: "8px", background: "#10b981" }} />
                <span style={{ fontSize: "12px", color: "#10b981", fontWeight: 500 }}>Cuenta activa</span>
              </div>
            </div>
          </div>
          <div className="ml-auto flex gap-3">
            {[
              { label: "Productos", value: stats?.total_products ?? "0" },
              { label: "Órdenes", value: stats?.total_orders ?? "0" },
              { label: "Clientes", value: stats?.total_customers ?? "0" },
            ].map(({ label, value }) => (
              <div key={label} className="text-center px-4 py-2 rounded-xl" style={{ background: "#f8fafc", border: "1px solid #f1f5f9" }}>
                <p style={{ fontSize: "18px", fontWeight: 700, color: "#0f172a" }}>{value}</p>
                <p style={{ fontSize: "11px", color: "#94a3b8" }}>{label}</p>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Info sections */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">
        {/* General info */}
        <div
          className="rounded-2xl p-5"
          style={{ background: "#fff", border: "1px solid #f1f5f9", boxShadow: "0 1px 8px rgba(0,0,0,0.04)" }}
        >
          <div className="flex items-center gap-2 mb-4">
            <Building2 size={16} style={{ color: "#6366f1" }} />
            <h3 style={{ fontSize: "14px", fontWeight: 600, color: "#0f172a" }}>Información general</h3>
          </div>
          <div className="space-y-3">
            <FormField 
              label="Nombre de empresa" 
              value={editData.name || ""} 
              onChange={(v) => updateEditField("name", v)} 
              editing={editing} 
              placeholder="Nombre de empresa"
            />
            <FormField 
              label="RFC / NIT" 
              value={editData.rfc} 
              onChange={(v) => updateEditField("rfc", v)} 
              editing={editing} 
              placeholder="ABC123456XYZ"
            />
            <FormField 
              label="Sector" 
              value={editData.sector} 
              onChange={(v) => updateEditField("sector", v)} 
              editing={editing} 
              placeholder="Moda, Electrónica, Alimentos..."
            />
          </div>
        </div>

        {/* Contact info */}
        <div
          className="rounded-2xl p-5"
          style={{ background: "#fff", border: "1px solid #f1f5f9", boxShadow: "0 1px 8px rgba(0,0,0,0.04)" }}
        >
          <div className="flex items-center gap-2 mb-4">
            <Phone size={16} style={{ color: "#10b981" }} />
            <h3 style={{ fontSize: "14px", fontWeight: 600, color: "#0f172a" }}>Datos de contacto</h3>
          </div>
          <div className="space-y-3">
            <FormField 
              label="Teléfono" 
              value={editData.phone} 
              onChange={(v) => updateEditField("phone", v)} 
              editing={editing} 
              placeholder="+52 1 55 1234 5678"
            />
            <FormField 
              label="Correo electrónico" 
              value={vendor.email} 
              editing={false} 
            />
            <FormField 
              label="Sitio web" 
              value={editData.website} 
              onChange={(v) => updateEditField("website", v)} 
              editing={editing} 
              placeholder="www.mitienda.com"
            />
          </div>
        </div>

        {/* Address */}
        <div
          className="rounded-2xl p-5"
          style={{ background: "#fff", border: "1px solid #f1f5f9", boxShadow: "0 1px 8px rgba(0,0,0,0.04)" }}
        >
          <div className="flex items-center gap-2 mb-4">
            <MapPin size={16} style={{ color: "#f59e0b" }} />
            <h3 style={{ fontSize: "14px", fontWeight: 600, color: "#0f172a" }}>Dirección fiscal</h3>
          </div>
          <div className="space-y-3">
            <FormField 
              label="Dirección" 
              value={editData.address} 
              onChange={(v) => updateEditField("address", v)} 
              editing={editing} 
              placeholder="Av. Insurgentes Sur 1234"
            />
            <div className="grid grid-cols-2 gap-3">
              <FormField 
                label="Ciudad" 
                value={editData.city} 
                onChange={(v) => updateEditField("city", v)} 
                editing={editing} 
                placeholder="México"
              />
              <FormField 
                label="Estado" 
                value={editData.state} 
                onChange={(v) => updateEditField("state", v)} 
                editing={editing} 
                placeholder="CDMX"
              />
            </div>
            <div className="grid grid-cols-2 gap-3">
              <FormField 
                label="C.P." 
                value={editData.postal_code} 
                onChange={(v) => updateEditField("postal_code", v)} 
                editing={editing} 
                placeholder="03100"
              />
              <FormField 
                label="País" 
                value={editData.country} 
                onChange={(v) => updateEditField("country", v)} 
                editing={editing} 
                placeholder="México"
              />
            </div>
          </div>
        </div>

        {/* Description */}
        <div
          className="rounded-2xl p-5"
          style={{ background: "#fff", border: "1px solid #f1f5f9", boxShadow: "0 1px 8px rgba(0,0,0,0.04)" }}
        >
          <div className="flex items-center gap-2 mb-4">
            <Globe size={16} style={{ color: "#8b5cf6" }} />
            <h3 style={{ fontSize: "14px", fontWeight: 600, color: "#0f172a" }}>Descripción del negocio</h3>
          </div>
          <div>
            <label className="block mb-1.5" style={{ fontSize: "12.5px", fontWeight: 600, color: "#475569" }}>
              Descripción
            </label>
            {editing ? (
              <textarea
                value={editData.description || ""}
                onChange={(e) => updateEditField("description", e.target.value)}
                rows={5}
                className="w-full rounded-xl px-4 py-2.5 outline-none resize-none"
                style={{ background: "#f8fafc", border: "1.5px solid #6366f1", fontSize: "13.5px", color: "#0f172a" }}
                placeholder="Describe tu negocio y qué productos/servicios ofreces"
              />
            ) : (
              <div
                className="rounded-xl px-4 py-3"
                style={{ background: "#f8fafc", border: "1px solid #f1f5f9", fontSize: "13.5px", color: "#374151", lineHeight: 1.7, minHeight: "120px" }}
              >
                {editData.description || <span style={{ color: "#cbd5e1" }}>Sin descripción</span>}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
