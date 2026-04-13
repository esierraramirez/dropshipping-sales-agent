import { useState } from "react";
import { Building2, MapPin, Phone, Globe, Mail, Camera, Save, Edit3, CheckCircle2 } from "lucide-react";

const initialData = {
  nombre: "Mi Moda Online",
  rfc: "MMO230401ABC",
  giro: "Dropshipping / Moda y Accesorios",
  telefono: "+52 1 55 1234 5678",
  email: "contacto@mimoda.mx",
  sitio: "www.mimoda.mx",
  direccion: "Av. Insurgentes Sur 1234, Col. Del Valle",
  ciudad: "Ciudad de México",
  estado: "CDMX",
  cp: "03100",
  pais: "México",
  descripcion: "Tienda de moda online especializada en ropa de mujer, accesorios y calzado. Distribuidores directos de fabricantes nacionales e internacionales con envíos a toda la república.",
};

function FormField({
  label,
  value,
  onChange,
  type = "text",
  placeholder,
  editing,
}: {
  label: string;
  value: string;
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
          value={value}
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
  const [data, setData] = useState(initialData);
  const [editing, setEditing] = useState(false);
  const [saved, setSaved] = useState(false);

  const handleSave = () => {
    setEditing(false);
    setSaved(true);
    setTimeout(() => setSaved(false), 3000);
  };

  const updateField = (field: keyof typeof initialData, value: string) => {
    setData((prev) => ({ ...prev, [field]: value }));
  };

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
          {editing ? (
            <button
              onClick={handleSave}
              className="flex items-center gap-2 rounded-xl px-5 py-2.5"
              style={{ background: "linear-gradient(135deg, #6366f1, #8b5cf6)", color: "#fff", fontSize: "13px", fontWeight: 600, border: "none", cursor: "pointer" }}
            >
              <Save size={14} />
              Guardar cambios
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
            {editing && (
              <button
                className="absolute -bottom-1 -right-1 rounded-lg flex items-center justify-center"
                style={{ width: "26px", height: "26px", background: "#0f172a", border: "2px solid #fff" }}
              >
                <Camera size={12} style={{ color: "#fff" }} />
              </button>
            )}
          </div>
          <div>
            <h2 style={{ fontSize: "20px", fontWeight: 700, color: "#0f172a" }}>{data.nombre}</h2>
            <p style={{ fontSize: "13px", color: "#94a3b8", marginTop: "2px" }}>{data.giro}</p>
            <div className="flex items-center gap-4 mt-3">
              <div className="flex items-center gap-1.5">
                <div className="rounded-full" style={{ width: "8px", height: "8px", background: "#10b981" }} />
                <span style={{ fontSize: "12px", color: "#10b981", fontWeight: 500 }}>Plan Pro activo</span>
              </div>
              <span style={{ fontSize: "12px", color: "#94a3b8" }}>Miembro desde Abr 2024</span>
            </div>
          </div>
          <div className="ml-auto flex gap-3">
            {[
              { label: "Productos", value: "1,248" },
              { label: "Órdenes", value: "342" },
              { label: "Clientes", value: "186" },
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
            <FormField label="Nombre de empresa" value={data.nombre} onChange={(v) => updateField("nombre", v)} editing={editing} />
            <FormField label="RFC / NIT" value={data.rfc} onChange={(v) => updateField("rfc", v)} editing={editing} />
            <FormField label="Giro / Sector" value={data.giro} onChange={(v) => updateField("giro", v)} editing={editing} />
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
            <FormField label="Teléfono" value={data.telefono} onChange={(v) => updateField("telefono", v)} editing={editing} />
            <FormField label="Correo electrónico" value={data.email} onChange={(v) => updateField("email", v)} type="email" editing={editing} />
            <FormField label="Sitio web" value={data.sitio} onChange={(v) => updateField("sitio", v)} editing={editing} />
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
            <FormField label="Dirección" value={data.direccion} onChange={(v) => updateField("direccion", v)} editing={editing} />
            <div className="grid grid-cols-2 gap-3">
              <FormField label="Ciudad" value={data.ciudad} onChange={(v) => updateField("ciudad", v)} editing={editing} />
              <FormField label="Estado" value={data.estado} onChange={(v) => updateField("estado", v)} editing={editing} />
            </div>
            <div className="grid grid-cols-2 gap-3">
              <FormField label="C.P." value={data.cp} onChange={(v) => updateField("cp", v)} editing={editing} />
              <FormField label="País" value={data.pais} onChange={(v) => updateField("pais", v)} editing={editing} />
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
                value={data.descripcion}
                onChange={(e) => updateField("descripcion", e.target.value)}
                rows={5}
                className="w-full rounded-xl px-4 py-2.5 outline-none resize-none"
                style={{ background: "#f8fafc", border: "1.5px solid #6366f1", fontSize: "13.5px", color: "#0f172a" }}
              />
            ) : (
              <div
                className="rounded-xl px-4 py-3"
                style={{ background: "#f8fafc", border: "1px solid #f1f5f9", fontSize: "13.5px", color: "#374151", lineHeight: 1.7 }}
              >
                {data.descripcion}
              </div>
            )}
          </div>

          {/* Subscription plan */}
          <div
            className="mt-4 rounded-xl p-4"
            style={{ background: "linear-gradient(135deg, rgba(99,102,241,0.08), rgba(139,92,246,0.06))", border: "1px solid rgba(99,102,241,0.15)" }}
          >
            <div className="flex items-center justify-between">
              <div>
                <p style={{ fontSize: "13px", fontWeight: 700, color: "#6366f1" }}>Plan Pro</p>
                <p style={{ fontSize: "11.5px", color: "#94a3b8", marginTop: "2px" }}>
                  Renovación: 13 May 2026
                </p>
              </div>
              <button
                className="rounded-lg px-3 py-1.5"
                style={{ background: "#6366f1", color: "#fff", fontSize: "12px", fontWeight: 600, border: "none", cursor: "pointer" }}
              >
                Gestionar plan
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
