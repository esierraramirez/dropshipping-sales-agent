import { Bell, Search, HelpCircle, ChevronDown } from "lucide-react";
import { useLocation } from "react-router";

const pageTitles: Record<string, { title: string; subtitle: string }> = {
  "/dashboard": { title: "Dashboard", subtitle: "Resumen general de tu negocio" },
  "/empresa": { title: "Mi Empresa", subtitle: "Gestiona la información de tu empresa" },
  "/catalogo": { title: "Catálogo de Productos", subtitle: "Administra tus productos y catálogos" },
  "/agente": { title: "Agente Inteligente", subtitle: "Configura y prueba tu asistente de IA" },
  "/ordenes": { title: "Órdenes", subtitle: "Gestiona los pedidos de tus clientes" },
  "/whatsapp": { title: "WhatsApp Business", subtitle: "Conexión y estado de WhatsApp API" },
  "/configuracion": { title: "Configuración", subtitle: "Ajusta tu cuenta y preferencias" },
};

export function Topbar() {
  const location = useLocation();
  const pageInfo = pageTitles[location.pathname] || { title: "DropSync", subtitle: "" };

  return (
    <header
      className="flex items-center justify-between px-6"
      style={{
        height: "72px",
        background: "#fff",
        borderBottom: "1px solid #f1f5f9",
        position: "sticky",
        top: 0,
        zIndex: 10,
      }}
    >
      {/* Page Title */}
      <div>
        <h1 style={{ fontSize: "18px", fontWeight: 600, color: "#0f172a", lineHeight: 1.2 }}>
          {pageInfo.title}
        </h1>
        <p style={{ fontSize: "12.5px", color: "#94a3b8", marginTop: "2px" }}>
          {pageInfo.subtitle}
        </p>
      </div>

      {/* Right side actions */}
      <div className="flex items-center gap-3">
        {/* Search */}
        <div
          className="flex items-center gap-2 rounded-xl px-3 py-2 cursor-pointer"
          style={{
            background: "#f8fafc",
            border: "1px solid #e2e8f0",
            width: "220px",
          }}
        >
          <Search size={14} style={{ color: "#94a3b8" }} />
          <span style={{ fontSize: "13px", color: "#94a3b8" }}>Buscar...</span>
          <div
            className="ml-auto rounded-md px-1.5 py-0.5"
            style={{ background: "#e2e8f0", fontSize: "10px", color: "#64748b" }}
          >
            ⌘K
          </div>
        </div>

        {/* Help */}
        <button
          className="flex items-center justify-center rounded-xl transition-all"
          style={{
            width: "38px",
            height: "38px",
            background: "#f8fafc",
            border: "1px solid #e2e8f0",
            color: "#94a3b8",
          }}
        >
          <HelpCircle size={16} />
        </button>

        {/* Notifications */}
        <button
          className="flex items-center justify-center rounded-xl transition-all relative"
          style={{
            width: "38px",
            height: "38px",
            background: "#f8fafc",
            border: "1px solid #e2e8f0",
            color: "#94a3b8",
          }}
        >
          <Bell size={16} />
          <span
            className="absolute top-2 right-2 rounded-full"
            style={{
              width: "7px",
              height: "7px",
              background: "#6366f1",
              border: "2px solid #fff",
            }}
          />
        </button>

        {/* Divider */}
        <div style={{ width: "1px", height: "28px", background: "#e2e8f0" }} />

        {/* User */}
        <div className="flex items-center gap-2 cursor-pointer rounded-xl px-2 py-1.5 transition-all"
          style={{ background: "transparent" }}
        >
          <div
            className="rounded-full flex items-center justify-center"
            style={{
              width: "32px",
              height: "32px",
              background: "linear-gradient(135deg, #6366f1, #8b5cf6)",
              flexShrink: 0,
            }}
          >
            <span style={{ color: "#fff", fontSize: "12px", fontWeight: 700 }}>JG</span>
          </div>
          <div>
            <p style={{ fontSize: "13px", fontWeight: 600, color: "#0f172a", lineHeight: 1.2 }}>
              Juan García
            </p>
            <p style={{ fontSize: "11px", color: "#94a3b8" }}>Tienda Mi Moda</p>
          </div>
          <ChevronDown size={14} style={{ color: "#94a3b8", marginLeft: "2px" }} />
        </div>
      </div>
    </header>
  );
}
