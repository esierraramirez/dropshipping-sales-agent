import { useState, useRef } from "react";
import {
  Upload,
  Search,
  Filter,
  Download,
  MoreHorizontal,
  Edit3,
  Trash2,
  Package,
  FileSpreadsheet,
  CheckCircle2,
  AlertTriangle,
  Eye,
  Plus,
  ChevronLeft,
  ChevronRight,
} from "lucide-react";

const mockProducts = [
  { id: 1, sku: "VES-001", nombre: "Vestido floral verano", categoria: "Vestidos", precio: 480, stock: 42, estado: "activo", imagen: "🌸" },
  { id: 2, sku: "BLU-002", nombre: "Blusa casual manga larga", categoria: "Blusas", precio: 290, stock: 87, estado: "activo", imagen: "👚" },
  { id: 3, sku: "JEA-003", nombre: "Jeans skinny mujer", categoria: "Pantalones", precio: 650, stock: 15, estado: "bajo_stock", imagen: "👖" },
  { id: 4, sku: "ZAP-004", nombre: "Zapatillas deportivas blancas", categoria: "Calzado", precio: 890, stock: 31, estado: "activo", imagen: "👟" },
  { id: 5, sku: "BOL-005", nombre: "Bolso cuero sintético negro", categoria: "Accesorios", precio: 1200, stock: 8, estado: "bajo_stock", imagen: "👜" },
  { id: 6, sku: "FAL-006", nombre: "Falda midi plisada", categoria: "Faldas", precio: 380, stock: 55, estado: "activo", imagen: "👗" },
  { id: 7, sku: "ACC-007", nombre: "Collar dorado minimalista", categoria: "Accesorios", precio: 180, stock: 120, estado: "activo", imagen: "📿" },
  { id: 8, sku: "SUD-008", nombre: "Sudadera oversized gris", categoria: "Sudaderas", precio: 540, stock: 0, estado: "sin_stock", imagen: "🩶" },
  { id: 9, sku: "VES-009", nombre: "Vestido elegante noche", categoria: "Vestidos", precio: 1450, stock: 22, estado: "activo", imagen: "✨" },
  { id: 10, sku: "BLU-010", nombre: "Blusa satinada botones", categoria: "Blusas", precio: 420, stock: 63, estado: "activo", imagen: "🪡" },
];

const estadoConfig: Record<string, { label: string; color: string; bg: string }> = {
  activo: { label: "Activo", color: "#10b981", bg: "rgba(16,185,129,0.1)" },
  bajo_stock: { label: "Bajo stock", color: "#f59e0b", bg: "rgba(245,158,11,0.1)" },
  sin_stock: { label: "Sin stock", color: "#ef4444", bg: "rgba(239,68,68,0.1)" },
};

export function CatalogoPage() {
  const [search, setSearch] = useState("");
  const [uploadState, setUploadState] = useState<"idle" | "uploading" | "success">("idle");
  const [uploadProgress, setUploadProgress] = useState(0);
  const [selectedCategory, setSelectedCategory] = useState("Todas");
  const [dragOver, setDragOver] = useState(false);
  const fileRef = useRef<HTMLInputElement>(null);

  const categories = ["Todas", "Vestidos", "Blusas", "Pantalones", "Calzado", "Accesorios", "Faldas", "Sudaderas"];

  const filtered = mockProducts.filter((p) => {
    const matchSearch =
      p.nombre.toLowerCase().includes(search.toLowerCase()) ||
      p.sku.toLowerCase().includes(search.toLowerCase()) ||
      p.categoria.toLowerCase().includes(search.toLowerCase());
    const matchCategory = selectedCategory === "Todas" || p.categoria === selectedCategory;
    return matchSearch && matchCategory;
  });

  const handleUpload = () => {
    setUploadState("uploading");
    setUploadProgress(0);
    const interval = setInterval(() => {
      setUploadProgress((prev) => {
        if (prev >= 100) {
          clearInterval(interval);
          setUploadState("success");
          return 100;
        }
        return prev + 10;
      });
    }, 150);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setDragOver(false);
    handleUpload();
  };

  return (
    <div className="space-y-5">
      {/* Stats row */}
      <div className="grid grid-cols-4 gap-4">
        {[
          { label: "Total productos", value: "1,248", icon: "📦", color: "#6366f1" },
          { label: "Activos", value: "1,180", icon: "✅", color: "#10b981" },
          { label: "Bajo stock", value: "52", icon: "⚠️", color: "#f59e0b" },
          { label: "Sin stock", value: "16", icon: "❌", color: "#ef4444" },
        ].map(({ label, value, icon, color }) => (
          <div
            key={label}
            className="rounded-2xl p-4 flex items-center gap-4"
            style={{ background: "#fff", border: "1px solid #f1f5f9", boxShadow: "0 1px 8px rgba(0,0,0,0.04)" }}
          >
            <div
              className="rounded-xl flex items-center justify-center text-xl shrink-0"
              style={{ width: "44px", height: "44px", background: `${color}12` }}
            >
              {icon}
            </div>
            <div>
              <p style={{ fontSize: "22px", fontWeight: 700, color: "#0f172a", lineHeight: 1 }}>{value}</p>
              <p style={{ fontSize: "12px", color: "#94a3b8", marginTop: "2px" }}>{label}</p>
            </div>
          </div>
        ))}
      </div>

      {/* Upload section */}
      <div
        className="rounded-2xl p-5"
        style={{ background: "#fff", border: "1px solid #f1f5f9", boxShadow: "0 1px 8px rgba(0,0,0,0.04)" }}
      >
        <div className="flex items-center gap-2 mb-4">
          <FileSpreadsheet size={16} style={{ color: "#10b981" }} />
          <h3 style={{ fontSize: "14px", fontWeight: 600, color: "#0f172a" }}>
            Importar catálogo desde Excel
          </h3>
        </div>

        {uploadState === "idle" && (
          <div
            className="rounded-2xl p-8 text-center cursor-pointer transition-all"
            style={{
              border: `2px dashed ${dragOver ? "#6366f1" : "#e2e8f0"}`,
              background: dragOver ? "rgba(99,102,241,0.04)" : "#fafbfc",
            }}
            onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
            onDragLeave={() => setDragOver(false)}
            onDrop={handleDrop}
            onClick={() => fileRef.current?.click()}
          >
            <input
              ref={fileRef}
              type="file"
              accept=".xlsx,.xls,.csv"
              className="hidden"
              onChange={handleUpload}
            />
            <div
              className="mx-auto rounded-2xl flex items-center justify-center mb-4"
              style={{ width: "56px", height: "56px", background: "rgba(99,102,241,0.1)" }}
            >
              <Upload size={24} style={{ color: "#6366f1" }} />
            </div>
            <p style={{ fontSize: "15px", fontWeight: 600, color: "#374151" }}>
              Arrastra tu archivo Excel aquí
            </p>
            <p style={{ fontSize: "13px", color: "#94a3b8", marginTop: "4px" }}>
              o haz clic para seleccionar · Soporta .xlsx, .xls, .csv
            </p>
            <button
              className="mt-4 rounded-xl px-5 py-2"
              style={{ background: "linear-gradient(135deg, #6366f1, #8b5cf6)", color: "#fff", fontSize: "13px", fontWeight: 600, border: "none", cursor: "pointer" }}
            >
              Seleccionar archivo
            </button>
          </div>
        )}

        {uploadState === "uploading" && (
          <div className="rounded-2xl p-6 text-center" style={{ background: "#fafbfc", border: "1px solid #e2e8f0" }}>
            <div
              className="mx-auto rounded-2xl flex items-center justify-center mb-4"
              style={{ width: "56px", height: "56px", background: "rgba(99,102,241,0.1)" }}
            >
              <FileSpreadsheet size={24} style={{ color: "#6366f1" }} />
            </div>
            <p style={{ fontSize: "14px", fontWeight: 600, color: "#374151", marginBottom: "4px" }}>
              Procesando catálogo.xlsx
            </p>
            <p style={{ fontSize: "12.5px", color: "#94a3b8", marginBottom: "16px" }}>
              Validando y cargando productos...
            </p>
            <div
              className="rounded-full overflow-hidden"
              style={{ height: "8px", background: "#e2e8f0" }}
            >
              <div
                className="h-full rounded-full transition-all duration-300"
                style={{ width: `${uploadProgress}%`, background: "linear-gradient(90deg, #6366f1, #8b5cf6)" }}
              />
            </div>
            <p style={{ fontSize: "12px", color: "#94a3b8", marginTop: "8px" }}>
              {uploadProgress}% completado
            </p>
          </div>
        )}

        {uploadState === "success" && (
          <div
            className="rounded-2xl p-5 flex items-center gap-4"
            style={{ background: "rgba(16,185,129,0.06)", border: "1px solid rgba(16,185,129,0.2)" }}
          >
            <div
              className="rounded-xl flex items-center justify-center shrink-0"
              style={{ width: "44px", height: "44px", background: "rgba(16,185,129,0.15)" }}
            >
              <CheckCircle2 size={22} style={{ color: "#10b981" }} />
            </div>
            <div className="flex-1">
              <p style={{ fontSize: "14px", fontWeight: 600, color: "#065f46" }}>
                Catálogo importado exitosamente
              </p>
              <p style={{ fontSize: "12.5px", color: "#6b7280", marginTop: "2px" }}>
                Se cargaron <strong>248 productos nuevos</strong> · 3 duplicados ignorados
              </p>
            </div>
            <button
              onClick={() => setUploadState("idle")}
              className="rounded-xl px-4 py-2"
              style={{ background: "#10b981", color: "#fff", fontSize: "12.5px", fontWeight: 600, border: "none", cursor: "pointer" }}
            >
              Importar otro
            </button>
          </div>
        )}

        {/* Template download */}
        <div className="flex items-center justify-between mt-4">
          <div className="flex items-center gap-2">
            <AlertTriangle size={13} style={{ color: "#f59e0b" }} />
            <span style={{ fontSize: "12px", color: "#94a3b8" }}>
              Usa nuestra plantilla para evitar errores de formato
            </span>
          </div>
          <button
            className="flex items-center gap-2 rounded-lg px-3 py-1.5"
            style={{ background: "#f8fafc", border: "1px solid #e2e8f0", color: "#374151", fontSize: "12px", fontWeight: 500, cursor: "pointer" }}
          >
            <Download size={12} />
            Descargar plantilla
          </button>
        </div>
      </div>

      {/* Products table */}
      <div
        className="rounded-2xl overflow-hidden"
        style={{ background: "#fff", border: "1px solid #f1f5f9", boxShadow: "0 1px 8px rgba(0,0,0,0.04)" }}
      >
        {/* Table header */}
        <div
          className="flex items-center gap-3 p-4"
          style={{ borderBottom: "1px solid #f1f5f9" }}
        >
          <h3 style={{ fontSize: "14px", fontWeight: 600, color: "#0f172a" }}>
            Productos ({filtered.length})
          </h3>

          <div className="flex-1 max-w-xs">
            <div
              className="flex items-center gap-2 rounded-xl px-3 py-2"
              style={{ background: "#f8fafc", border: "1px solid #e2e8f0" }}
            >
              <Search size={13} style={{ color: "#94a3b8" }} />
              <input
                type="text"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                placeholder="Buscar producto, SKU..."
                className="flex-1 outline-none bg-transparent"
                style={{ fontSize: "13px", color: "#0f172a" }}
              />
            </div>
          </div>

          {/* Category filter */}
          <div className="flex items-center gap-2 overflow-x-auto">
            {categories.slice(0, 5).map((cat) => (
              <button
                key={cat}
                onClick={() => setSelectedCategory(cat)}
                className="rounded-lg px-3 py-1.5 whitespace-nowrap"
                style={{
                  background: selectedCategory === cat ? "#6366f1" : "#f8fafc",
                  color: selectedCategory === cat ? "#fff" : "#64748b",
                  border: selectedCategory === cat ? "none" : "1px solid #e2e8f0",
                  fontSize: "12px",
                  fontWeight: 500,
                  cursor: "pointer",
                }}
              >
                {cat}
              </button>
            ))}
          </div>

          <div className="ml-auto flex items-center gap-2">
            <button
              className="flex items-center gap-2 rounded-xl px-4 py-2"
              style={{ background: "linear-gradient(135deg, #6366f1, #8b5cf6)", color: "#fff", fontSize: "12.5px", fontWeight: 600, border: "none", cursor: "pointer" }}
            >
              <Plus size={13} />
              Nuevo producto
            </button>
          </div>
        </div>

        {/* Table */}
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr style={{ background: "#f8fafc", borderBottom: "1px solid #f1f5f9" }}>
                {["", "SKU", "Producto", "Categoría", "Precio", "Stock", "Estado", ""].map((h) => (
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
              {filtered.map((product, i) => {
                const estado = estadoConfig[product.estado];
                return (
                  <tr
                    key={product.id}
                    className="transition-all"
                    style={{
                      borderBottom: i < filtered.length - 1 ? "1px solid #f8fafc" : "none",
                    }}
                    onMouseEnter={(e) => (e.currentTarget.style.background = "#fafbfc")}
                    onMouseLeave={(e) => (e.currentTarget.style.background = "transparent")}
                  >
                    <td className="px-4 py-3">
                      <div
                        className="flex items-center justify-center rounded-lg text-xl"
                        style={{ width: "36px", height: "36px", background: "#f8fafc" }}
                      >
                        {product.imagen}
                      </div>
                    </td>
                    <td className="px-4 py-3">
                      <span
                        className="rounded-lg px-2 py-1"
                        style={{ background: "#f1f5f9", color: "#64748b", fontSize: "11.5px", fontWeight: 600, fontFamily: "monospace" }}
                      >
                        {product.sku}
                      </span>
                    </td>
                    <td className="px-4 py-3">
                      <p style={{ fontSize: "13.5px", fontWeight: 500, color: "#0f172a" }}>{product.nombre}</p>
                    </td>
                    <td className="px-4 py-3">
                      <span style={{ fontSize: "13px", color: "#64748b" }}>{product.categoria}</span>
                    </td>
                    <td className="px-4 py-3">
                      <span style={{ fontSize: "13.5px", fontWeight: 600, color: "#0f172a" }}>
                        ${product.precio.toLocaleString()}
                      </span>
                    </td>
                    <td className="px-4 py-3">
                      <div className="flex items-center gap-2">
                        <div
                          className="rounded-full"
                          style={{
                            height: "6px",
                            width: `${Math.min((product.stock / 120) * 60, 60)}px`,
                            background:
                              product.stock === 0 ? "#ef4444" :
                              product.stock < 20 ? "#f59e0b" : "#10b981",
                            minWidth: "4px",
                          }}
                        />
                        <span style={{ fontSize: "13px", color: "#374151", fontWeight: 500 }}>
                          {product.stock}
                        </span>
                      </div>
                    </td>
                    <td className="px-4 py-3">
                      <div
                        className="flex items-center gap-1.5 rounded-full px-2.5 py-1 w-fit"
                        style={{ background: estado.bg, color: estado.color }}
                      >
                        <span style={{ fontSize: "11.5px", fontWeight: 600 }}>{estado.label}</span>
                      </div>
                    </td>
                    <td className="px-4 py-3">
                      <div className="flex items-center gap-2">
                        <button
                          className="rounded-lg p-1.5 transition-all"
                          style={{ background: "transparent", border: "none", color: "#94a3b8", cursor: "pointer" }}
                        >
                          <Eye size={14} />
                        </button>
                        <button
                          className="rounded-lg p-1.5 transition-all"
                          style={{ background: "transparent", border: "none", color: "#94a3b8", cursor: "pointer" }}
                        >
                          <Edit3 size={14} />
                        </button>
                        <button
                          className="rounded-lg p-1.5 transition-all"
                          style={{ background: "transparent", border: "none", color: "#94a3b8", cursor: "pointer" }}
                        >
                          <Trash2 size={14} />
                        </button>
                      </div>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>

        {/* Pagination */}
        <div
          className="flex items-center justify-between px-4 py-3"
          style={{ borderTop: "1px solid #f1f5f9" }}
        >
          <span style={{ fontSize: "12.5px", color: "#94a3b8" }}>
            Mostrando {filtered.length} de 1,248 productos
          </span>
          <div className="flex items-center gap-2">
            <button className="rounded-lg p-1.5" style={{ background: "#f8fafc", border: "1px solid #e2e8f0", color: "#94a3b8", cursor: "pointer" }}>
              <ChevronLeft size={14} />
            </button>
            {[1, 2, 3, "...", 125].map((page, i) => (
              <button
                key={i}
                className="rounded-lg px-3 py-1.5"
                style={{
                  background: page === 1 ? "#6366f1" : "#f8fafc",
                  border: page === 1 ? "none" : "1px solid #e2e8f0",
                  color: page === 1 ? "#fff" : "#64748b",
                  fontSize: "12.5px",
                  fontWeight: 500,
                  cursor: "pointer",
                }}
              >
                {page}
              </button>
            ))}
            <button className="rounded-lg p-1.5" style={{ background: "#f8fafc", border: "1px solid #e2e8f0", color: "#94a3b8", cursor: "pointer" }}>
              <ChevronRight size={14} />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
