import { NavLink, useNavigate } from "react-router";
import {
  LayoutDashboard,
  Building2,
  Package,
  Bot,
  ShoppingCart,
  MessageCircle,
  Settings,
  ChevronLeft,
  ChevronRight,
  Zap,
  LogOut,
} from "lucide-react";
import { useState } from "react";
import { clearAuthState, getCurrentVendor } from "../../lib/auth";

const navItems = [
  { to: "/dashboard", icon: LayoutDashboard, label: "Dashboard" },
  { to: "/empresa", icon: Building2, label: "Mi Empresa" },
  { to: "/catalogo", icon: Package, label: "Catálogo" },
  { to: "/agente", icon: Bot, label: "Agente Inteligente" },
  { to: "/ordenes", icon: ShoppingCart, label: "Órdenes" },
  { to: "/whatsapp", icon: MessageCircle, label: "WhatsApp" },
];

const bottomItems = [
  { to: "/configuracion", icon: Settings, label: "Configuración" },
];

interface SidebarProps {
  collapsed: boolean;
  onToggle: () => void;
}

export function Sidebar({ collapsed, onToggle }: SidebarProps) {
  const navigate = useNavigate();
  const vendor = getCurrentVendor();

  // Get initials from vendor name for avatar
  const getInitials = (name: string) => {
    return name
      .split(" ")
      .map((word) => word[0])
      .join("")
      .toUpperCase()
      .slice(0, 2);
  };

  const handleLogout = () => {
    clearAuthState();
    navigate("/login");
  };

  return (
    <aside
      className="flex flex-col h-full transition-all duration-300"
      style={{
        width: collapsed ? "72px" : "240px",
        background: "linear-gradient(180deg, #0f172a 0%, #1e293b 100%)",
        borderRight: "1px solid rgba(255,255,255,0.06)",
      }}
    >
      {/* Logo */}
      <div
        className="flex items-center px-4 py-5"
        style={{ borderBottom: "1px solid rgba(255,255,255,0.06)", minHeight: "72px" }}
      >
        <div
          className="flex items-center justify-center rounded-xl shrink-0"
          style={{
            width: "36px",
            height: "36px",
            background: "linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)",
          }}
        >
          <Zap size={18} color="#fff" />
        </div>
        {!collapsed && (
          <div className="ml-3 overflow-hidden">
            <span
              className="block whitespace-nowrap"
              style={{ color: "#fff", fontWeight: 700, fontSize: "16px", letterSpacing: "-0.3px" }}
            >
              DropSync
            </span>
            <span
              className="block whitespace-nowrap"
              style={{ color: "#94a3b8", fontSize: "11px", fontWeight: 400 }}
            >
              Panel Administrativo
            </span>
          </div>
        )}
      </div>

      {/* Nav Items */}
      <nav className="flex-1 py-4 overflow-hidden">
        <div className="px-3 space-y-1">
          {navItems.map(({ to, icon: Icon, label }) => (
            <NavLink
              key={to}
              to={to}
              className={({ isActive }) =>
                `flex items-center gap-3 rounded-xl px-3 py-2.5 transition-all duration-150 group ${
                  isActive
                    ? "sidebar-nav-active"
                    : "sidebar-nav-item"
                }`
              }
              style={({ isActive }) => ({
                background: isActive
                  ? "linear-gradient(135deg, rgba(99,102,241,0.2) 0%, rgba(139,92,246,0.15) 100%)"
                  : "transparent",
                border: isActive ? "1px solid rgba(99,102,241,0.3)" : "1px solid transparent",
                color: isActive ? "#a5b4fc" : "#94a3b8",
              })}
            >
              <Icon
                size={18}
                style={{ flexShrink: 0 }}
              />
              {!collapsed && (
                <span
                  className="whitespace-nowrap overflow-hidden text-ellipsis"
                  style={{ fontSize: "13.5px", fontWeight: 500 }}
                >
                  {label}
                </span>
              )}
            </NavLink>
          ))}
        </div>
      </nav>

      {/* Bottom Items */}
      <div style={{ borderTop: "1px solid rgba(255,255,255,0.06)" }} className="py-3">
        <div className="px-3 space-y-1">
          {bottomItems.map(({ to, icon: Icon, label }) => (
            <NavLink
              key={to}
              to={to}
              className={({ isActive }) =>
                `flex items-center gap-3 rounded-xl px-3 py-2.5 transition-all duration-150`
              }
              style={({ isActive }) => ({
                background: isActive
                  ? "linear-gradient(135deg, rgba(99,102,241,0.2) 0%, rgba(139,92,246,0.15) 100%)"
                  : "transparent",
                border: isActive ? "1px solid rgba(99,102,241,0.3)" : "1px solid transparent",
                color: isActive ? "#a5b4fc" : "#94a3b8",
              })}
            >
              <Icon size={18} style={{ flexShrink: 0 }} />
              {!collapsed && (
                <span style={{ fontSize: "13.5px", fontWeight: 500, whiteSpace: "nowrap" }}>
                  {label}
                </span>
              )}
            </NavLink>
          ))}

          {/* User info + logout */}
          <div
            className="flex items-center gap-3 rounded-xl px-3 py-2.5 mt-2 cursor-pointer transition-all duration-150"
            style={{ color: "#64748b" }}
            onClick={handleLogout}
            title="Cerrar sesión"
          >
            <div
              className="rounded-full flex items-center justify-center shrink-0"
              style={{
                width: "28px",
                height: "28px",
                background: "linear-gradient(135deg, #6366f1, #8b5cf6)",
              }}
            >
              <span style={{ color: "#fff", fontSize: "11px", fontWeight: 700 }}>
                {getInitials(vendor?.name || "Usuario")}
              </span>
            </div>
            {!collapsed && (
              <div className="flex-1 overflow-hidden">
                <p style={{ color: "#e2e8f0", fontSize: "12.5px", fontWeight: 500, whiteSpace: "nowrap" }}>
                  {vendor?.name || "Mi Empresa"}
                </p>
                <p style={{ color: "#475569", fontSize: "11px", whiteSpace: "nowrap" }}>
                  {vendor?.email || "empresa@email.com"}
                </p>
              </div>
            )}
            {!collapsed && <LogOut size={14} style={{ color: "#475569", flexShrink: 0 }} />}
          </div>
        </div>

        {/* Collapse toggle */}
        <div className="px-3 mt-2">
          <button
            onClick={onToggle}
            className="w-full flex items-center justify-center rounded-xl py-2 transition-all duration-150"
            style={{
              background: "rgba(255,255,255,0.04)",
              border: "1px solid rgba(255,255,255,0.06)",
              color: "#475569",
            }}
          >
            {collapsed ? <ChevronRight size={14} /> : (
              <div className="flex items-center gap-2">
                <ChevronLeft size={14} />
                <span style={{ fontSize: "11px" }}>Colapsar</span>
              </div>
            )}
          </button>
        </div>
      </div>
    </aside>
  );
}
