import {
  Package,
  ShoppingCart,
  Bot,
  MessageCircle,
  TrendingUp,
  TrendingDown,
  ArrowUpRight,
  Clock,
  CheckCircle2,
  AlertCircle,
  XCircle,
  RefreshCw,
} from "lucide-react";
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  BarChart,
  Bar,
} from "recharts";

const salesData = [
  { day: "Lun", ventas: 12400, ordenes: 8 },
  { day: "Mar", ventas: 18200, ordenes: 14 },
  { day: "Mié", ventas: 9800, ordenes: 6 },
  { day: "Jue", ventas: 24600, ordenes: 19 },
  { day: "Vie", ventas: 31200, ordenes: 26 },
  { day: "Sáb", ventas: 28900, ordenes: 22 },
  { day: "Dom", ventas: 16700, ordenes: 13 },
];

const topProducts = [
  { name: "Vestido floral verano", ventas: 148, stock: 42, trend: "up" },
  { name: "Blusa casual manga larga", ventas: 112, stock: 87, trend: "up" },
  { name: "Jeans skinny mujer", ventas: 98, stock: 15, trend: "down" },
  { name: "Zapatillas deportivas", ventas: 76, stock: 31, trend: "up" },
  { name: "Bolso cuero sintético", ventas: 64, stock: 8, trend: "down" },
];

const recentOrders = [
  { id: "#ORD-4821", client: "María López", total: "$1,240", status: "entregado", time: "hace 5 min" },
  { id: "#ORD-4820", client: "Carlos Reyes", total: "$890", status: "en_proceso", time: "hace 18 min" },
  { id: "#ORD-4819", client: "Ana García", total: "$2,150", status: "pendiente", time: "hace 32 min" },
  { id: "#ORD-4818", client: "Luis Morales", total: "$650", status: "entregado", time: "hace 1h" },
  { id: "#ORD-4817", client: "Sofia Ruiz", total: "$3,200", status: "cancelado", time: "hace 2h" },
];

const statusConfig: Record<string, { label: string; color: string; bg: string; icon: React.ReactNode }> = {
  entregado: {
    label: "Entregado",
    color: "#10b981",
    bg: "rgba(16,185,129,0.1)",
    icon: <CheckCircle2 size={12} />,
  },
  en_proceso: {
    label: "En proceso",
    color: "#f59e0b",
    bg: "rgba(245,158,11,0.1)",
    icon: <RefreshCw size={12} />,
  },
  pendiente: {
    label: "Pendiente",
    color: "#6366f1",
    bg: "rgba(99,102,241,0.1)",
    icon: <Clock size={12} />,
  },
  cancelado: {
    label: "Cancelado",
    color: "#ef4444",
    bg: "rgba(239,68,68,0.1)",
    icon: <XCircle size={12} />,
  },
};

function MetricCard({
  icon: Icon,
  label,
  value,
  change,
  changeType,
  subtitle,
  accent,
}: {
  icon: React.ElementType;
  label: string;
  value: string;
  change?: string;
  changeType?: "up" | "down";
  subtitle?: string;
  accent: string;
}) {
  return (
    <div
      className="rounded-2xl p-5 relative overflow-hidden"
      style={{ background: "#fff", border: "1px solid #f1f5f9", boxShadow: "0 1px 8px rgba(0,0,0,0.04)" }}
    >
      <div className="flex items-start justify-between mb-4">
        <div
          className="flex items-center justify-center rounded-xl"
          style={{ width: "44px", height: "44px", background: `${accent}15` }}
        >
          <Icon size={20} style={{ color: accent }} />
        </div>
        {change && (
          <div
            className="flex items-center gap-1 rounded-full px-2.5 py-1"
            style={{
              background: changeType === "up" ? "rgba(16,185,129,0.1)" : "rgba(239,68,68,0.1)",
              color: changeType === "up" ? "#10b981" : "#ef4444",
            }}
          >
            {changeType === "up" ? <TrendingUp size={12} /> : <TrendingDown size={12} />}
            <span style={{ fontSize: "11px", fontWeight: 600 }}>{change}</span>
          </div>
        )}
      </div>
      <p style={{ fontSize: "28px", fontWeight: 700, color: "#0f172a", letterSpacing: "-0.5px" }}>
        {value}
      </p>
      <p style={{ fontSize: "13px", color: "#94a3b8", marginTop: "4px" }}>{label}</p>
      {subtitle && (
        <p style={{ fontSize: "11.5px", color: "#cbd5e1", marginTop: "6px" }}>{subtitle}</p>
      )}
    </div>
  );
}

function StatusBadge({ status }: { status: string }) {
  const config = statusConfig[status];
  return (
    <div
      className="flex items-center gap-1.5 rounded-full px-2.5 py-1 w-fit"
      style={{ background: config.bg, color: config.color }}
    >
      {config.icon}
      <span style={{ fontSize: "11.5px", fontWeight: 600 }}>{config.label}</span>
    </div>
  );
}

export function DashboardPage() {
  return (
    <div className="space-y-6">
      {/* Welcome banner */}
      <div
        className="rounded-2xl p-6 flex items-center justify-between"
        style={{
          background: "linear-gradient(135deg, #6366f1 0%, #8b5cf6 60%, #a78bfa 100%)",
          boxShadow: "0 8px 32px rgba(99,102,241,0.25)",
        }}
      >
        <div>
          <p style={{ color: "rgba(255,255,255,0.75)", fontSize: "13px", marginBottom: "4px" }}>
            Buenos días 👋
          </p>
          <h2 style={{ color: "#fff", fontSize: "22px", fontWeight: 700, letterSpacing: "-0.5px" }}>
            Tienda Mi Moda
          </h2>
          <p style={{ color: "rgba(255,255,255,0.65)", fontSize: "13px", marginTop: "4px" }}>
            Hoy tienes 8 órdenes nuevas por atender
          </p>
        </div>
        <div className="flex items-center gap-3">
          <div
            className="rounded-xl px-4 py-2.5 cursor-pointer"
            style={{ background: "rgba(255,255,255,0.15)", border: "1px solid rgba(255,255,255,0.25)" }}
          >
            <span style={{ color: "#fff", fontSize: "13px", fontWeight: 600 }}>Ver órdenes</span>
          </div>
          <div style={{ fontSize: "52px" }}>📦</div>
        </div>
      </div>

      {/* Metric Cards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <MetricCard
          icon={Package}
          label="Productos activos"
          value="1,248"
          change="+12%"
          changeType="up"
          subtitle="Último catálogo: hace 2 días"
          accent="#6366f1"
        />
        <MetricCard
          icon={ShoppingCart}
          label="Órdenes este mes"
          value="342"
          change="+24%"
          changeType="up"
          subtitle="108 órdenes esta semana"
          accent="#10b981"
        />
        <MetricCard
          icon={Bot}
          label="Agente IA"
          value="Activo"
          subtitle="Respondió 89 consultas hoy"
          accent="#f59e0b"
        />
        <MetricCard
          icon={MessageCircle}
          label="WhatsApp"
          value="Conectado"
          subtitle="+52 1 (55) 1234-5678"
          accent="#25D366"
        />
      </div>

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        {/* Sales chart */}
        <div
          className="lg:col-span-2 rounded-2xl p-5"
          style={{ background: "#fff", border: "1px solid #f1f5f9", boxShadow: "0 1px 8px rgba(0,0,0,0.04)" }}
        >
          <div className="flex items-center justify-between mb-5">
            <div>
              <h3 style={{ fontSize: "15px", fontWeight: 600, color: "#0f172a" }}>
                Ventas de la semana
              </h3>
              <p style={{ fontSize: "12px", color: "#94a3b8", marginTop: "2px" }}>
                Total: $141,800 MXN
              </p>
            </div>
            <div
              className="flex items-center gap-1 rounded-lg px-3 py-1.5 cursor-pointer"
              style={{ background: "#f8fafc", border: "1px solid #e2e8f0" }}
            >
              <span style={{ fontSize: "12px", color: "#64748b" }}>Esta semana</span>
              <ArrowUpRight size={13} style={{ color: "#94a3b8" }} />
            </div>
          </div>
          <ResponsiveContainer width="100%" height={220}>
            <AreaChart data={salesData}>
              <defs>
                <linearGradient id="salesGradient" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#6366f1" stopOpacity={0.15} />
                  <stop offset="95%" stopColor="#6366f1" stopOpacity={0} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
              <XAxis
                dataKey="day"
                tick={{ fontSize: 12, fill: "#94a3b8" }}
                axisLine={false}
                tickLine={false}
              />
              <YAxis
                tick={{ fontSize: 11, fill: "#94a3b8" }}
                axisLine={false}
                tickLine={false}
                tickFormatter={(v) => `$${(v / 1000).toFixed(0)}k`}
              />
              <Tooltip
                contentStyle={{
                  background: "#0f172a",
                  border: "none",
                  borderRadius: "12px",
                  fontSize: "12px",
                  color: "#e2e8f0",
                }}
                formatter={(v: number) => [`$${v.toLocaleString()}`, "Ventas"]}
              />
              <Area
                type="monotone"
                dataKey="ventas"
                stroke="#6366f1"
                strokeWidth={2.5}
                fill="url(#salesGradient)"
                dot={{ fill: "#6366f1", strokeWidth: 2, r: 4 }}
              />
            </AreaChart>
          </ResponsiveContainer>
        </div>

        {/* Orders by day */}
        <div
          className="rounded-2xl p-5"
          style={{ background: "#fff", border: "1px solid #f1f5f9", boxShadow: "0 1px 8px rgba(0,0,0,0.04)" }}
        >
          <div className="mb-5">
            <h3 style={{ fontSize: "15px", fontWeight: 600, color: "#0f172a" }}>
              Órdenes por día
            </h3>
            <p style={{ fontSize: "12px", color: "#94a3b8", marginTop: "2px" }}>
              Esta semana: 108 pedidos
            </p>
          </div>
          <ResponsiveContainer width="100%" height={220}>
            <BarChart data={salesData} barSize={18}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" vertical={false} />
              <XAxis
                dataKey="day"
                tick={{ fontSize: 12, fill: "#94a3b8" }}
                axisLine={false}
                tickLine={false}
              />
              <YAxis
                tick={{ fontSize: 11, fill: "#94a3b8" }}
                axisLine={false}
                tickLine={false}
              />
              <Tooltip
                contentStyle={{
                  background: "#0f172a",
                  border: "none",
                  borderRadius: "12px",
                  fontSize: "12px",
                  color: "#e2e8f0",
                }}
              />
              <Bar dataKey="ordenes" fill="#8b5cf6" radius={[6, 6, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Bottom Row */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        {/* Recent orders */}
        <div
          className="lg:col-span-2 rounded-2xl p-5"
          style={{ background: "#fff", border: "1px solid #f1f5f9", boxShadow: "0 1px 8px rgba(0,0,0,0.04)" }}
        >
          <div className="flex items-center justify-between mb-5">
            <h3 style={{ fontSize: "15px", fontWeight: 600, color: "#0f172a" }}>
              Órdenes recientes
            </h3>
            <a href="/ordenes" style={{ fontSize: "12.5px", color: "#6366f1", fontWeight: 600 }}>
              Ver todas →
            </a>
          </div>
          <div className="space-y-3">
            {recentOrders.map((order) => (
              <div
                key={order.id}
                className="flex items-center gap-4 rounded-xl px-4 py-3 transition-all"
                style={{ background: "#f8fafc", border: "1px solid #f1f5f9" }}
              >
                <div>
                  <p style={{ fontSize: "13px", fontWeight: 600, color: "#0f172a" }}>{order.id}</p>
                  <p style={{ fontSize: "11.5px", color: "#94a3b8" }}>{order.client}</p>
                </div>
                <div className="ml-auto flex items-center gap-4">
                  <p style={{ fontSize: "13px", fontWeight: 600, color: "#0f172a" }}>
                    {order.total}
                  </p>
                  <StatusBadge status={order.status} />
                  <p style={{ fontSize: "11px", color: "#94a3b8", minWidth: "60px", textAlign: "right" }}>
                    {order.time}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Top Products */}
        <div
          className="rounded-2xl p-5"
          style={{ background: "#fff", border: "1px solid #f1f5f9", boxShadow: "0 1px 8px rgba(0,0,0,0.04)" }}
        >
          <div className="flex items-center justify-between mb-5">
            <h3 style={{ fontSize: "15px", fontWeight: 600, color: "#0f172a" }}>
              Top productos
            </h3>
            <span
              className="rounded-full px-2 py-0.5"
              style={{ background: "rgba(99,102,241,0.1)", color: "#6366f1", fontSize: "11px", fontWeight: 600 }}
            >
              Esta semana
            </span>
          </div>
          <div className="space-y-4">
            {topProducts.map((product, i) => (
              <div key={product.name} className="flex items-center gap-3">
                <span
                  className="flex items-center justify-center rounded-lg shrink-0"
                  style={{
                    width: "26px",
                    height: "26px",
                    background: i === 0 ? "#fef3c7" : i === 1 ? "#e0e7ff" : "#f1f5f9",
                    color: i === 0 ? "#f59e0b" : i === 1 ? "#6366f1" : "#94a3b8",
                    fontSize: "11px",
                    fontWeight: 700,
                  }}
                >
                  {i + 1}
                </span>
                <div className="flex-1 min-w-0">
                  <p
                    style={{ fontSize: "12.5px", fontWeight: 500, color: "#0f172a", whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis" }}
                  >
                    {product.name}
                  </p>
                  <p style={{ fontSize: "11px", color: "#94a3b8" }}>
                    {product.ventas} vendidos · Stock: {product.stock}
                  </p>
                </div>
                {product.trend === "up" ? (
                  <TrendingUp size={14} style={{ color: "#10b981", flexShrink: 0 }} />
                ) : (
                  <TrendingDown size={14} style={{ color: "#ef4444", flexShrink: 0 }} />
                )}
              </div>
            ))}
          </div>

          {/* Quick stats */}
          <div
            className="mt-5 rounded-xl p-3"
            style={{ background: "rgba(99,102,241,0.05)", border: "1px solid rgba(99,102,241,0.1)" }}
          >
            <p style={{ fontSize: "11.5px", color: "#6366f1", fontWeight: 600, marginBottom: "6px" }}>
              Estado del sistema
            </p>
            <div className="space-y-1.5">
              {[
                { label: "Agente IA", status: "Activo", ok: true },
                { label: "WhatsApp API", status: "Conectado", ok: true },
                { label: "Sincronización", status: "En pausa", ok: false },
              ].map(({ label, status, ok }) => (
                <div key={label} className="flex items-center justify-between">
                  <span style={{ fontSize: "11.5px", color: "#64748b" }}>{label}</span>
                  <div className="flex items-center gap-1.5">
                    <div
                      className="rounded-full"
                      style={{
                        width: "6px",
                        height: "6px",
                        background: ok ? "#10b981" : "#f59e0b",
                      }}
                    />
                    <span style={{ fontSize: "11px", color: ok ? "#10b981" : "#f59e0b", fontWeight: 500 }}>
                      {status}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
