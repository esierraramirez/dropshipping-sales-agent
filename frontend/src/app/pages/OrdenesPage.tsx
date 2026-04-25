import { useState, useEffect } from "react";
import {
  Search,
  Filter,
  Eye,
  ChevronDown,
  Clock,
  CheckCircle2,
  XCircle,
  RefreshCw,
  Truck,
  Package,
  MapPin,
  Phone,
  X,
} from "lucide-react";
import { api } from "../lib/api";

interface OrderItem {
  product_id: string;
  product_name: string;
  quantity: number;
  unit_price: number;
}

interface Order {
  id: number;
  customer_name: string;
  customer_phone: string;
  customer_address?: string;
  items: OrderItem[];
  total_amount: number;
  status: string;
  created_at: string;
}

interface OrderRow {
  id: string;
  cliente: string;
  telefono: string;
  direccion: string;
  productos: Array<{ nombre: string; qty: number; precio: number }>;
  total: number;
  estado: string;
  fecha: string;
  hora: string;
  pago: string;
  notas: string;
}

const mockOrders: OrderRow[] = [
  {
    id: "#ORD-4821",
    cliente: "María López",
    telefono: "+52 55 1234 5678",
    direccion: "Av. Reforma 123, Col. Centro, CDMX",
    productos: [
      { nombre: "Vestido floral verano", qty: 1, precio: 480 },
      { nombre: "Collar dorado minimalista", qty: 2, precio: 180 },
    ],
    total: 840,
    estado: "entregado",
    fecha: "13 Abr 2026",
    hora: "09:15",
    pago: "Tarjeta",
    notas: "",
  },
  {
    id: "#ORD-4820",
    cliente: "Carlos Reyes",
    telefono: "+52 33 9876 5432",
    direccion: "Calle Morelos 456, Col. Americana, Guadalajara",
    productos: [
      { nombre: "Jeans skinny mujer", qty: 1, precio: 650 },
      { nombre: "Blusa casual manga larga", qty: 1, precio: 290 },
    ],
    total: 940,
    estado: "en_proceso",
    fecha: "13 Abr 2026",
    hora: "08:42",
    pago: "Transferencia",
    notas: "Entregar en horario matutino",
  },
  {
    id: "#ORD-4819",
    cliente: "Ana García",
    telefono: "+52 81 4567 8901",
    direccion: "Blvd. Constitución 789, Col. Contry, Monterrey",
    productos: [
      { nombre: "Bolso cuero sintético negro", qty: 1, precio: 1200 },
      { nombre: "Zapatillas deportivas blancas", qty: 1, precio: 890 },
    ],
    total: 2090,
    estado: "pendiente",
    fecha: "13 Abr 2026",
    hora: "08:10",
    pago: "PayPal",
    notas: "",
  },
  {
    id: "#ORD-4818",
    cliente: "Luis Morales",
    telefono: "+52 55 2345 6789",
    direccion: "Calle Insurgentes 321, Col. San Ángel, CDMX",
    productos: [
      { nombre: "Falda midi plisada", qty: 1, precio: 380 },
      { nombre: "Blusa satinada botones", qty: 1, precio: 420 },
    ],
    total: 800,
    estado: "enviado",
    fecha: "12 Abr 2026",
    hora: "16:30",
    pago: "Efectivo",
    notas: "Dejar con el portero",
  },
  {
    id: "#ORD-4817",
    cliente: "Sofía Ruiz",
    telefono: "+52 33 3456 7890",
    direccion: "Av. Vallarta 1500, Zapopan, Jalisco",
    productos: [
      { nombre: "Vestido elegante noche", qty: 1, precio: 1450 },
      { nombre: "Bolso cuero sintético negro", qty: 1, precio: 1200 },
      { nombre: "Collar dorado minimalista", qty: 3, precio: 180 },
    ],
    total: 3190,
    estado: "cancelado",
    fecha: "12 Abr 2026",
    hora: "13:20",
    pago: "Tarjeta",
    notas: "Cancelado por el cliente",
  },
  {
    id: "#ORD-4816",
    cliente: "Roberto Sánchez",
    telefono: "+52 55 5678 9012",
    direccion: "Periférico Sur 890, Col. Pedregal, CDMX",
    productos: [
      { nombre: "Sudadera oversized gris", qty: 2, precio: 540 },
    ],
    total: 1080,
    estado: "entregado",
    fecha: "12 Abr 2026",
    hora: "11:05",
    pago: "Transferencia",
    notas: "",
  },
];

type OrderStatus = "en_proceso" | "enviado" | "entregado" | "cancelado";

const statusConfig: Record<string, { label: string; color: string; bg: string; icon: React.ReactNode }> = {
  entregado: { label: "Entregado", color: "#10b981", bg: "rgba(16,185,129,0.1)", icon: <CheckCircle2 size={12} /> },
  en_proceso: { label: "En proceso", color: "#f59e0b", bg: "rgba(245,158,11,0.1)", icon: <RefreshCw size={12} /> },
  enviado: { label: "Enviado", color: "#3b82f6", bg: "rgba(59,130,246,0.1)", icon: <Truck size={12} /> },
  cancelado: { label: "Cancelado", color: "#ef4444", bg: "rgba(239,68,68,0.1)", icon: <XCircle size={12} /> },
};

const allStatuses = ["Todos", "en_proceso", "enviado", "entregado", "cancelado"];

function StatusBadge({ status }: { status: string }) {
  const cfg = statusConfig[status];
  return (
    <div
      className="flex items-center gap-1.5 rounded-full px-2.5 py-1 w-fit"
      style={{ background: cfg.bg, color: cfg.color }}
    >
      {cfg.icon}
      <span style={{ fontSize: "11.5px", fontWeight: 600 }}>{cfg.label}</span>
    </div>
  );
}

export function OrdenesPage() {
  const [search, setSearch] = useState("");
  const [filterStatus, setFilterStatus] = useState("Todos");
  const [selectedOrder, setSelectedOrder] = useState<OrderRow | null>(null);
  const [orders, setOrders] = useState<OrderRow[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [orderStatuses, setOrderStatuses] = useState<Record<string, string>>({});

  // Cargar órdenes del backend
  useEffect(() => {
    const loadOrders = async () => {
      try {
        setLoading(true);
        setError(null);
        const response = await api.get<{ orders: Order[] }>("/orders/me", true);
        
        // Mapear órdenes del backend al formato del frontend
        const mappedOrders = response.orders.map((order) => {
          const date = new Date(order.created_at);
          return {
            id: `#ORD-${order.id}`,
            cliente: order.customer_name,
            telefono: order.customer_phone,
            direccion: order.customer_address || "",
            productos: order.items.map((item) => ({
              nombre: item.product_name,
              qty: item.quantity,
              precio: item.unit_price,
            })),
            total: order.total_amount,
            estado: mapBackendStatus(order.status),
            fecha: date.toLocaleDateString("es-MX", { year: "numeric", month: "short", day: "numeric" }),
            hora: date.toLocaleTimeString("es-MX", { hour: "2-digit", minute: "2-digit" }),
            pago: "Pendiente",
            notas: "",
          };
        });

        setOrders(mappedOrders);
        setOrderStatuses(Object.fromEntries(mappedOrders.map((o) => [o.id, o.estado])));
      } catch (err) {
        console.error("Error cargando órdenes:", err);
        setError("No se pudieron cargar las órdenes");
        setOrders([]);
      } finally {
        setLoading(false);
      }
    };

    loadOrders();
  }, []);

  // Mapear estados del backend al frontend
  const mapBackendStatus = (status: string): string => {
    const mapping: Record<string, string> = {
      pending: "en_proceso",
      confirmed: "en_proceso",
      processed: "en_proceso",
      shipped: "enviado",
      delivered: "entregado",
      cancelled: "cancelado",
      en_proceso: "en_proceso",
      enviado: "enviado",
      entregado: "entregado",
      cancelado: "cancelado",
    };
    return mapping[status] || "en_proceso";
  };

  const filtered = orders.filter((o) => {
    const matchSearch =
      o.id.toLowerCase().includes(search.toLowerCase()) ||
      o.cliente.toLowerCase().includes(search.toLowerCase());
    const matchStatus = filterStatus === "Todos" || orderStatuses[o.id] === filterStatus;
    return matchSearch && matchStatus;
  });

  // Mapear estados del frontend al backend
  const mapToBackendStatus = (status: string): string => {
    const mapping: Record<string, string> = {
      en_proceso: "en_proceso",
      enviado: "enviado",
      entregado: "entregado",
      cancelado: "cancelado",
    };
    return mapping[status] || "en_proceso";
  };

  const updateStatus = async (orderId: string, newStatus: string) => {
    try {
      const numId = parseInt(orderId.replace("#ORD-", ""));
      const backendStatus = mapToBackendStatus(newStatus);
      await api.patch(`/orders/me/${numId}/status`, { status: backendStatus }, true);
      setOrderStatuses((prev) => ({ ...prev, [orderId]: newStatus }));
      if (selectedOrder?.id === orderId) {
        setSelectedOrder((prev) => prev ? { ...prev, estado: newStatus } : null);
      }
    } catch (err) {
      console.error("Error actualizando estado:", err);
      // Revertir cambio en caso de error
      alert("Error al actualizar el estado");
    }
  };

  const statusCounts = {
    en_proceso: orders.filter((o) => orderStatuses[o.id] === "en_proceso").length,
    enviado: orders.filter((o) => orderStatuses[o.id] === "enviado").length,
    entregado: orders.filter((o) => orderStatuses[o.id] === "entregado").length,
    cancelado: orders.filter((o) => orderStatuses[o.id] === "cancelado").length,
  };

  if (loading) {
    return (
      <div className="space-y-5">
        <div className="flex items-center justify-center h-96">
          <div style={{ textAlign: "center" }}>
            <div style={{ fontSize: "32px", marginBottom: "10px" }}>📦</div>
            <p style={{ color: "#64748b", marginBottom: "4px" }}>Cargando órdenes...</p>
            <p style={{ fontSize: "13px", color: "#94a3b8" }}>Un momento por favor</p>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="space-y-5">
        <div className="flex items-center justify-center h-96">
          <div style={{ textAlign: "center" }}>
            <div style={{ fontSize: "32px", marginBottom: "10px" }}>⚠️</div>
            <p style={{ color: "#ef4444", marginBottom: "4px" }}>{error}</p>
            <p style={{ fontSize: "13px", color: "#94a3b8" }}>Verifica tu conexión e intenta de nuevo</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-5">
      {/* Summary cards */}
      <div className="grid grid-cols-5 gap-3">
        {(["en_proceso", "enviado", "entregado", "cancelado"] as const).map((s) => {
          const cfg = statusConfig[s];
          return (
            <div
              key={s}
              className="rounded-2xl p-4 cursor-pointer transition-all"
              style={{
                background: "#fff",
                border: filterStatus === s ? `1.5px solid ${cfg.color}` : "1px solid #f1f5f9",
                boxShadow: "0 1px 8px rgba(0,0,0,0.04)",
              }}
              onClick={() => setFilterStatus(filterStatus === s ? "Todos" : s)}
            >
              <div className="flex items-center justify-between mb-2">
                <div
                  className="rounded-lg flex items-center justify-center"
                  style={{ width: "28px", height: "28px", background: cfg.bg, color: cfg.color }}
                >
                  {cfg.icon}
                </div>
                <span
                  style={{ fontSize: "20px", fontWeight: 700, color: cfg.color }}
                >
                  {statusCounts[s]}
                </span>
              </div>
              <p style={{ fontSize: "11.5px", color: "#94a3b8", fontWeight: 500 }}>{cfg.label}</p>
            </div>
          );
        })}
      </div>

      {/* Main table */}
      <div
        className="rounded-2xl overflow-hidden"
        style={{ background: "#fff", border: "1px solid #f1f5f9", boxShadow: "0 1px 8px rgba(0,0,0,0.04)" }}
      >
        {/* Table toolbar */}
        <div className="flex items-center gap-3 p-4" style={{ borderBottom: "1px solid #f1f5f9" }}>
          <h3 style={{ fontSize: "14px", fontWeight: 600, color: "#0f172a" }}>
            Órdenes ({filtered.length})
          </h3>

          <div
            className="flex items-center gap-2 rounded-xl px-3 py-2 max-w-xs"
            style={{ background: "#f8fafc", border: "1px solid #e2e8f0" }}
          >
            <Search size={13} style={{ color: "#94a3b8" }} />
            <input
              type="text"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Buscar orden o cliente..."
              className="outline-none bg-transparent flex-1"
              style={{ fontSize: "13px", color: "#0f172a" }}
            />
          </div>

          <div className="flex items-center gap-2">
            {allStatuses.slice(0, 4).map((s) => (
              <button
                key={s}
                onClick={() => setFilterStatus(s)}
                className="rounded-lg px-3 py-1.5"
                style={{
                  background: filterStatus === s ? "#6366f1" : "#f8fafc",
                  color: filterStatus === s ? "#fff" : "#64748b",
                  border: filterStatus === s ? "none" : "1px solid #e2e8f0",
                  fontSize: "12px",
                  fontWeight: 500,
                  cursor: "pointer",
                  textTransform: "capitalize",
                }}
              >
                {s === "Todos" ? "Todos" : statusConfig[s]?.label}
              </button>
            ))}
          </div>
        </div>

        {/* Table */}
        <table className="w-full">
          <thead>
            <tr style={{ background: "#f8fafc", borderBottom: "1px solid #f1f5f9" }}>
              {["Orden", "Cliente", "Productos", "Total", "Estado", "Fecha", "Acciones"].map((h) => (
                <th
                  key={h}
                  className="text-left px-4 py-3"
                  style={{ fontSize: "11.5px", fontWeight: 600, color: "#94a3b8", textTransform: "uppercase", letterSpacing: "0.05em" }}
                >
                  {h}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {filtered.map((order, i) => (
              <tr
                key={order.id}
                className="transition-all"
                style={{ borderBottom: i < filtered.length - 1 ? "1px solid #f8fafc" : "none" }}
                onMouseEnter={(e) => (e.currentTarget.style.background = "#fafbfc")}
                onMouseLeave={(e) => (e.currentTarget.style.background = "transparent")}
              >
                <td className="px-4 py-3">
                  <span style={{ fontSize: "13px", fontWeight: 700, color: "#6366f1", fontFamily: "monospace" }}>
                    {order.id}
                  </span>
                </td>
                <td className="px-4 py-3">
                  <p style={{ fontSize: "13.5px", fontWeight: 500, color: "#0f172a" }}>{order.cliente}</p>
                  <p style={{ fontSize: "11.5px", color: "#94a3b8" }}>{order.telefono}</p>
                </td>
                <td className="px-4 py-3">
                  <p style={{ fontSize: "13px", color: "#374151" }}>
                    {order.productos.length} producto{order.productos.length > 1 ? "s" : ""}
                  </p>
                  <p style={{ fontSize: "11.5px", color: "#94a3b8" }}>
                    {order.productos[0].nombre.slice(0, 22)}...
                  </p>
                </td>
                <td className="px-4 py-3">
                  <span style={{ fontSize: "14px", fontWeight: 700, color: "#0f172a" }}>
                    ${order.total.toLocaleString()}
                  </span>
                  <p style={{ fontSize: "11.5px", color: "#94a3b8" }}>{order.pago}</p>
                </td>
                <td className="px-4 py-3">
                  <StatusBadge status={orderStatuses[order.id]} />
                </td>
                <td className="px-4 py-3">
                  <p style={{ fontSize: "13px", color: "#374151" }}>{order.fecha}</p>
                  <p style={{ fontSize: "11.5px", color: "#94a3b8" }}>{order.hora}</p>
                </td>
                <td className="px-4 py-3">
                  <button
                    onClick={() => setSelectedOrder(order)}
                    className="flex items-center gap-1.5 rounded-lg px-3 py-1.5 transition-all"
                    style={{ background: "rgba(99,102,241,0.08)", color: "#6366f1", border: "none", cursor: "pointer", fontSize: "12px", fontWeight: 600 }}
                  >
                    <Eye size={13} />
                    Ver detalle
                  </button>
                </td>
              </tr>
            ))}
            {filtered.length === 0 && (
              <tr>
                <td colSpan={7} style={{ textAlign: "center", padding: "40px" }}>
                  <div style={{ color: "#94a3b8" }}>
                    <div style={{ fontSize: "28px", marginBottom: "8px" }}>📭</div>
                    <p style={{ fontSize: "14px", fontWeight: 500, marginBottom: "4px" }}>
                      {orders.length === 0 ? "No hay órdenes registradas" : "No hay resultados"}
                    </p>
                    <p style={{ fontSize: "12px", color: "#cbd5e1" }}>
                      {orders.length === 0 ? "Las órdenes aparecerán aquí después de que se concrete una venta en el chat" : "Intenta con otros filtros o términos de búsqueda"}
                    </p>
                  </div>
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      {/* Order Detail Modal */}
      {selectedOrder && (
        <div
          className="fixed inset-0 flex items-center justify-end"
          style={{ background: "rgba(0,0,0,0.4)", zIndex: 50 }}
          onClick={(e) => e.target === e.currentTarget && setSelectedOrder(null)}
        >
          <div
            className="h-full overflow-y-auto"
            style={{
              width: "440px",
              background: "#fff",
              boxShadow: "-8px 0 40px rgba(0,0,0,0.12)",
            }}
          >
            {/* Header */}
            <div
              className="flex items-center justify-between p-5"
              style={{ borderBottom: "1px solid #f1f5f9", position: "sticky", top: 0, background: "#fff", zIndex: 1 }}
            >
              <div>
                <h3 style={{ fontSize: "16px", fontWeight: 700, color: "#0f172a" }}>
                  Detalle de orden
                </h3>
                <p style={{ fontSize: "13px", color: "#6366f1", fontWeight: 600 }}>
                  {selectedOrder.id}
                </p>
              </div>
              <button
                onClick={() => setSelectedOrder(null)}
                className="rounded-xl p-2"
                style={{ background: "#f8fafc", border: "1px solid #e2e8f0", color: "#64748b", cursor: "pointer" }}
              >
                <X size={16} />
              </button>
            </div>

            <div className="p-5 space-y-5">
              {/* Status change */}
              <div className="rounded-xl p-4" style={{ background: "#f8fafc", border: "1px solid #f1f5f9" }}>
                <p style={{ fontSize: "12.5px", fontWeight: 600, color: "#475569", marginBottom: "10px" }}>
                  CAMBIAR ESTADO
                </p>
                <div className="flex flex-wrap gap-2">
                  {(["en_proceso", "enviado", "entregado", "cancelado"] as const).map((s) => {
                    const cfg = statusConfig[s];
                    const isActive = orderStatuses[selectedOrder.id] === s;
                    return (
                      <button
                        key={s}
                        onClick={() => updateStatus(selectedOrder.id, s)}
                        className="flex items-center gap-1.5 rounded-full px-3 py-1.5 transition-all"
                        style={{
                          background: isActive ? cfg.bg : "#fff",
                          color: isActive ? cfg.color : "#94a3b8",
                          border: isActive ? `1.5px solid ${cfg.color}` : "1.5px solid #e2e8f0",
                          fontSize: "12px",
                          fontWeight: 600,
                          cursor: "pointer",
                        }}
                      >
                        {cfg.icon}
                        {cfg.label}
                      </button>
                    );
                  })}
                </div>
              </div>

              {/* Client info */}
              <div>
                <p style={{ fontSize: "12.5px", fontWeight: 600, color: "#475569", marginBottom: "10px" }}>
                  INFORMACIÓN DEL CLIENTE
                </p>
                <div className="space-y-2">
                  <div className="flex items-center gap-3 rounded-xl p-3" style={{ background: "#f8fafc" }}>
                    <div
                      className="rounded-full flex items-center justify-center shrink-0"
                      style={{ width: "36px", height: "36px", background: "linear-gradient(135deg, #6366f1, #8b5cf6)" }}
                    >
                      <span style={{ color: "#fff", fontSize: "13px", fontWeight: 700 }}>
                        {selectedOrder.cliente.split(" ").map(n => n[0]).join("")}
                      </span>
                    </div>
                    <div>
                      <p style={{ fontSize: "14px", fontWeight: 600, color: "#0f172a" }}>{selectedOrder.cliente}</p>
                      <p style={{ fontSize: "12px", color: "#94a3b8" }}>Cliente registrado</p>
                    </div>
                  </div>
                  <div className="flex items-center gap-2 px-3 py-2">
                    <Phone size={13} style={{ color: "#94a3b8" }} />
                    <span style={{ fontSize: "13px", color: "#374151" }}>{selectedOrder.telefono}</span>
                  </div>
                  <div className="flex items-start gap-2 px-3 py-2">
                    <MapPin size={13} style={{ color: "#94a3b8", marginTop: "2px" }} />
                    <span style={{ fontSize: "13px", color: "#374151", lineHeight: 1.5 }}>{selectedOrder.direccion}</span>
                  </div>
                </div>
              </div>

              {/* Products */}
              <div>
                <p style={{ fontSize: "12.5px", fontWeight: 600, color: "#475569", marginBottom: "10px" }}>
                  PRODUCTOS ORDENADOS
                </p>
                <div className="space-y-2">
                  {selectedOrder.productos.map((product, i) => (
                    <div
                      key={i}
                      className="flex items-center gap-3 rounded-xl p-3"
                      style={{ background: "#f8fafc", border: "1px solid #f1f5f9" }}
                    >
                      <div
                        className="rounded-lg flex items-center justify-center text-lg shrink-0"
                        style={{ width: "40px", height: "40px", background: "#fff" }}
                      >
                        📦
                      </div>
                      <div className="flex-1">
                        <p style={{ fontSize: "13px", fontWeight: 500, color: "#0f172a" }}>{product.nombre}</p>
                        <p style={{ fontSize: "11.5px", color: "#94a3b8" }}>Qty: {product.qty}</p>
                      </div>
                      <p style={{ fontSize: "13.5px", fontWeight: 700, color: "#0f172a" }}>
                        ${(product.precio * product.qty).toLocaleString()}
                      </p>
                    </div>
                  ))}
                </div>
              </div>

              {/* Summary */}
              <div className="rounded-xl p-4" style={{ background: "rgba(99,102,241,0.05)", border: "1px solid rgba(99,102,241,0.12)" }}>
                <div className="space-y-2">
                  <div className="flex justify-between">
                    <span style={{ fontSize: "13px", color: "#64748b" }}>Subtotal</span>
                    <span style={{ fontSize: "13px", color: "#374151" }}>${selectedOrder.total.toLocaleString()}</span>
                  </div>
                  <div className="flex justify-between">
                    <span style={{ fontSize: "13px", color: "#64748b" }}>Envío</span>
                    <span style={{ fontSize: "13px", color: "#10b981", fontWeight: 600 }}>Gratis</span>
                  </div>
                  <div className="flex justify-between pt-2" style={{ borderTop: "1px solid rgba(99,102,241,0.15)" }}>
                    <span style={{ fontSize: "14px", fontWeight: 700, color: "#0f172a" }}>Total</span>
                    <span style={{ fontSize: "16px", fontWeight: 700, color: "#6366f1" }}>
                      ${selectedOrder.total.toLocaleString()}
                    </span>
                  </div>
                </div>
              </div>

              {/* Payment & notes */}
              <div className="grid grid-cols-2 gap-3">
                <div className="rounded-xl p-3" style={{ background: "#f8fafc" }}>
                  <p style={{ fontSize: "11.5px", color: "#94a3b8", marginBottom: "4px" }}>MÉTODO DE PAGO</p>
                  <p style={{ fontSize: "13.5px", fontWeight: 600, color: "#374151" }}>{selectedOrder.pago}</p>
                </div>
                <div className="rounded-xl p-3" style={{ background: "#f8fafc" }}>
                  <p style={{ fontSize: "11.5px", color: "#94a3b8", marginBottom: "4px" }}>FECHA</p>
                  <p style={{ fontSize: "13.5px", fontWeight: 600, color: "#374151" }}>
                    {selectedOrder.fecha} · {selectedOrder.hora}
                  </p>
                </div>
              </div>

              {selectedOrder.notas && (
                <div className="rounded-xl p-4" style={{ background: "#fffbeb", border: "1px solid #fde68a" }}>
                  <p style={{ fontSize: "12px", fontWeight: 600, color: "#92400e", marginBottom: "4px" }}>NOTAS</p>
                  <p style={{ fontSize: "13px", color: "#78350f" }}>{selectedOrder.notas}</p>
                </div>
              )}

              {/* Actions */}
              <div className="flex gap-3">
                <button
                  className="flex-1 flex items-center justify-center gap-2 rounded-xl py-2.5"
                  style={{ background: "linear-gradient(135deg, #6366f1, #8b5cf6)", color: "#fff", border: "none", cursor: "pointer", fontSize: "13px", fontWeight: 600 }}
                >
                  <Truck size={14} />
                  Notificar envío
                </button>
                <button
                  className="flex items-center justify-center rounded-xl px-4 py-2.5"
                  style={{ background: "#f8fafc", border: "1px solid #e2e8f0", color: "#374151", cursor: "pointer", fontSize: "13px", fontWeight: 600 }}
                >
                  <Package size={14} />
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
