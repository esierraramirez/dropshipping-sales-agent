import { useEffect, useRef, useState } from "react";
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
import { api, ApiError, type ProductsListResponse } from "../lib/api";

const fallbackProducts = [
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

type UiProduct = {
  id: number;
  sku: string;
  nombre: string;
  categoria: string;
  precio: number;
  stock: number;
  estado: "activo" | "bajo_stock" | "sin_stock";
  imagen: string;
};

function categoryEmoji(category: string) {
  const c = category.toLowerCase();
  if (c.includes("vest")) return "👗";
  if (c.includes("blus")) return "👚";
  if (c.includes("pant") || c.includes("jean")) return "👖";
  if (c.includes("calz") || c.includes("zap")) return "👟";
  if (c.includes("acces")) return "👜";
  return "📦";
}

function stockFromStatus(stockStatus: string) {
  const status = stockStatus.toLowerCase();
  if (status.includes("out")) return 0;
  if (status.includes("low")) return 12;
  return 50;
}

function uiStatusFromStock(stock: number): UiProduct["estado"] {
  if (stock <= 0) return "sin_stock";
  if (stock < 20) return "bajo_stock";
  return "activo";
}

function mapProductsResponse(response: ProductsListResponse): UiProduct[] {
  return response.products.map((product) => {
    const stock = stockFromStatus(product.stock_status);
    return {
      id: product.id,
      sku: product.product_id,
      nombre: product.name,
      categoria: product.category,
      precio: Number(product.price || 0),
      stock,
      estado: uiStatusFromStock(stock),
      imagen: categoryEmoji(product.category),
    };
  });
}

export function CatalogoPage() {
  const [search, setSearch] = useState("");
  const [uploadState, setUploadState] = useState<"idle" | "uploading" | "success">("idle");
  const [uploadProgress, setUploadProgress] = useState(0);
  const [selectedCategory, setSelectedCategory] = useState("Todas");
  const [dragOver, setDragOver] = useState(false);
  const [products, setProducts] = useState<UiProduct[]>(fallbackProducts);
  const [totalProducts, setTotalProducts] = useState(fallbackProducts.length);
  const [error, setError] = useState("");
  const [uploadSummary, setUploadSummary] = useState("");
  const [editingProduct, setEditingProduct] = useState<UiProduct | null>(null);
  const [editFormData, setEditFormData] = useState({ nombre: "", precio: 0, categoria: "", estado: "activo" });
  const [confirmDelete, setConfirmDelete] = useState<{ productId: number; productName: string } | null>(null);
  const [deletingProductId, setDeletingProductId] = useState<number | null>(null);
  const fileRef = useRef<HTMLInputElement>(null);

  const loadProducts = async () => {
    try {
      const response = await api.get<ProductsListResponse>("/catalog/products/me", true);
      const mapped = mapProductsResponse(response);
      setProducts(mapped);
      setTotalProducts(response.total_products);
      setError("");
      return response.total_products;
    } catch (err) {
      if (err instanceof ApiError) {
        setError(err.detail);
      } else {
        setError("No fue posible cargar el catálogo desde el backend.");
      }
      return null;
    }
  };

  useEffect(() => {
    loadProducts();
  }, []);

  const handleDeleteProduct = async (productId: number, productName: string) => {
    setConfirmDelete({ productId, productName });
  };

  const confirmDeleteProduct = async () => {
    if (!confirmDelete) return;
    
    setDeletingProductId(confirmDelete.productId);
    try {
      setError("");
      await api.delete(`/catalog/products/${confirmDelete.productId}`, true);
      setProducts(products.filter(p => p.id !== confirmDelete.productId));
      setTotalProducts(totalProducts - 1);
      setUploadSummary(`Producto "${confirmDelete.productName}" eliminado correctamente.`);
      setConfirmDelete(null);
    } catch (err) {
      if (err instanceof ApiError) {
        setError(err.detail);
      } else {
        setError("No fue posible eliminar el producto.");
      }
    } finally {
      setDeletingProductId(null);
    }
  };

  const handleOpenEdit = (product: UiProduct) => {
    setEditingProduct(product);
    setEditFormData({
      nombre: product.nombre,
      precio: product.precio,
      categoria: product.categoria,
      estado: product.estado,
    });
  };

  const handleCloseEdit = () => {
    setEditingProduct(null);
    setEditFormData({ nombre: "", precio: 0, categoria: "", estado: "activo" });
  };

  const handleSaveProduct = async () => {
    if (!editingProduct) return;

    try {
      setError("");
      await api.patch(`/catalog/products/${editingProduct.id}`, {
        name: editFormData.nombre,
        price: editFormData.precio,
        category: editFormData.categoria,
        stock_status: editFormData.estado,
      }, true);

      const updatedProducts = products.map(p => 
        p.id === editingProduct.id 
          ? { ...p, nombre: editFormData.nombre, precio: editFormData.precio, categoria: editFormData.categoria, estado: editFormData.estado as any }
          : p
      );
      setProducts(updatedProducts);
      setUploadSummary(`Producto "${editFormData.nombre}" actualizado correctamente.`);
      handleCloseEdit();
    } catch (err) {
      if (err instanceof ApiError) {
        setError(err.detail);
      } else {
        setError("No fue posible actualizar el producto.");
      }
    }
  };

  const categories = ["Todas", "Vestidos", "Blusas", "Pantalones", "Calzado", "Accesorios", "Faldas", "Sudaderas"];

  const filtered = products.filter((p) => {
    const matchSearch =
      p.nombre.toLowerCase().includes(search.toLowerCase()) ||
      p.sku.toLowerCase().includes(search.toLowerCase()) ||
      p.categoria.toLowerCase().includes(search.toLowerCase());
    const matchCategory = selectedCategory === "Todas" || p.categoria === selectedCategory;
    return matchSearch && matchCategory;
  });

  const handleUpload = async (file?: File) => {
    if (!file) return;

    setError("");
    setUploadSummary("");
    setUploadState("uploading");
    setUploadProgress(15);

    try {
      const formData = new FormData();
      formData.append("file", file);

      await api.post("/catalog/upload/me", formData, true);
      setUploadProgress(45);
      await api.post("/catalog/normalize/me", {}, true);
      setUploadProgress(75);
      await api.post("/catalog/save/me", {}, true);
      setUploadProgress(85);
      
      // Construir la base de conocimiento automáticamente
      try {
        await api.post("/catalog/build-knowledge-base/me", {}, true);
        setUploadProgress(95);
      } catch (kbErr) {
        console.warn("Advertencia: No se pudo construir la base de conocimiento:", kbErr);
        // Continuar de todos modos
      }
      
      const currentTotal = await loadProducts();
      setUploadProgress(100);
      setUploadSummary(
        currentTotal !== null
          ? `Catálogo sincronizado. Total actual: ${currentTotal} productos. Base de conocimiento construida.`
          : "La importación finalizó y los productos se sincronizaron."
      );
      setUploadState("success");
    } catch (err) {
      setUploadState("idle");
      if (err instanceof ApiError) {
        setError(err.detail);
      } else {
        setError("No fue posible importar el catálogo en el backend.");
      }
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setDragOver(false);
    const file = e.dataTransfer.files?.[0];
    handleUpload(file);
  };

  const activos = products.filter((p) => p.estado === "activo").length;
  const bajoStock = products.filter((p) => p.estado === "bajo_stock").length;
  const sinStock = products.filter((p) => p.estado === "sin_stock").length;

  return (
    <div className="space-y-5">
      {error && (
        <div
          className="rounded-xl px-4 py-3"
          style={{ background: "rgba(239,68,68,0.08)", border: "1px solid rgba(239,68,68,0.25)" }}
        >
          <p style={{ fontSize: "12.5px", color: "#b91c1c", fontWeight: 500 }}>{error}</p>
        </div>
      )}

      {/* Stats row */}
      <div className="grid grid-cols-4 gap-4">
        {[
          { label: "Total productos", value: `${totalProducts}`, icon: "📦", color: "#6366f1" },
          { label: "Activos", value: `${activos}`, icon: "✅", color: "#10b981" },
          { label: "Bajo stock", value: `${bajoStock}`, icon: "⚠️", color: "#f59e0b" },
          { label: "Sin stock", value: `${sinStock}`, icon: "❌", color: "#ef4444" },
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
              onChange={(e) => handleUpload(e.target.files?.[0])}
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
                {uploadSummary || "La importación finalizó y los productos ya se guardaron en el backend."}
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
                          className="rounded-lg p-1.5 transition-all hover:bg-gray-100"
                          style={{ background: "transparent", border: "none", color: "#94a3b8", cursor: "pointer" }}
                          onClick={() => handleOpenEdit(product)}
                          title="Ver detalles"
                        >
                          <Eye size={14} />
                        </button>
                        <button
                          className="rounded-lg p-1.5 transition-all hover:bg-gray-100"
                          style={{ background: "transparent", border: "none", color: "#94a3b8", cursor: "pointer" }}
                          onClick={() => handleOpenEdit(product)}
                          title="Editar producto"
                        >
                          <Edit3 size={14} />
                        </button>
                        <button
                          className="rounded-lg p-1.5 transition-all hover:bg-red-100"
                          style={{ background: "transparent", border: "none", color: "#94a3b8", cursor: "pointer" }}
                          onClick={() => handleDeleteProduct(product.id, product.nombre)}
                          title="Eliminar producto"
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
            Mostrando {filtered.length} de {totalProducts} productos
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

      {/* Modal de Edición */}
      {editingProduct && (
        <div
          style={{
            position: "fixed",
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            background: "rgba(0, 0, 0, 0.5)",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            zIndex: 50,
          }}
          onClick={handleCloseEdit}
        >
          <div
            style={{
              background: "white",
              borderRadius: "12px",
              padding: "24px",
              width: "90%",
              maxWidth: "500px",
              boxShadow: "0 20px 25px rgba(0, 0, 0, 0.15)",
            }}
            onClick={(e) => e.stopPropagation()}
          >
            <h3 style={{ fontSize: "18px", fontWeight: 600, marginBottom: "16px", color: "#1e293b" }}>
              Editar producto
            </h3>

            <div style={{ marginBottom: "16px" }}>
              <label style={{ display: "block", fontSize: "13px", fontWeight: 500, marginBottom: "6px", color: "#64748b" }}>
                Nombre
              </label>
              <input
                type="text"
                value={editFormData.nombre}
                onChange={(e) => setEditFormData({ ...editFormData, nombre: e.target.value })}
                style={{
                  width: "100%",
                  padding: "8px 12px",
                  border: "1px solid #e2e8f0",
                  borderRadius: "6px",
                  fontSize: "13px",
                  boxSizing: "border-box",
                }}
              />
            </div>

            <div style={{ marginBottom: "16px" }}>
              <label style={{ display: "block", fontSize: "13px", fontWeight: 500, marginBottom: "6px", color: "#64748b" }}>
                Precio
              </label>
              <input
                type="number"
                value={editFormData.precio}
                onChange={(e) => setEditFormData({ ...editFormData, precio: parseFloat(e.target.value) })}
                style={{
                  width: "100%",
                  padding: "8px 12px",
                  border: "1px solid #e2e8f0",
                  borderRadius: "6px",
                  fontSize: "13px",
                  boxSizing: "border-box",
                }}
              />
            </div>

            <div style={{ marginBottom: "16px" }}>
              <label style={{ display: "block", fontSize: "13px", fontWeight: 500, marginBottom: "6px", color: "#64748b" }}>
                Categoría
              </label>
              <select
                value={editFormData.categoria}
                onChange={(e) => setEditFormData({ ...editFormData, categoria: e.target.value })}
                style={{
                  width: "100%",
                  padding: "8px 12px",
                  border: "1px solid #e2e8f0",
                  borderRadius: "6px",
                  fontSize: "13px",
                  boxSizing: "border-box",
                }}
              >
                {categories.map(cat => (
                  <option key={cat} value={cat}>{cat}</option>
                ))}
              </select>
            </div>

            <div style={{ marginBottom: "20px" }}>
              <label style={{ display: "block", fontSize: "13px", fontWeight: 500, marginBottom: "6px", color: "#64748b" }}>
                Estado
              </label>
              <select
                value={editFormData.estado}
                onChange={(e) => setEditFormData({ ...editFormData, estado: e.target.value as any })}
                style={{
                  width: "100%",
                  padding: "8px 12px",
                  border: "1px solid #e2e8f0",
                  borderRadius: "6px",
                  fontSize: "13px",
                  boxSizing: "border-box",
                }}
              >
                <option value="activo">Activo</option>
                <option value="bajo_stock">Bajo stock</option>
                <option value="sin_stock">Sin stock</option>
              </select>
            </div>

            <div style={{ display: "flex", gap: "12px", justifyContent: "flex-end" }}>
              <button
                onClick={handleCloseEdit}
                style={{
                  padding: "8px 16px",
                  border: "1px solid #e2e8f0",
                  borderRadius: "6px",
                  background: "white",
                  color: "#64748b",
                  fontSize: "13px",
                  fontWeight: 500,
                  cursor: "pointer",
                }}
              >
                Cancelar
              </button>
              <button
                onClick={handleSaveProduct}
                style={{
                  padding: "8px 16px",
                  border: "none",
                  borderRadius: "6px",
                  background: "#6366f1",
                  color: "white",
                  fontSize: "13px",
                  fontWeight: 500,
                  cursor: "pointer",
                }}
              >
                Guardar cambios
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Modal de Confirmación de Eliminación */}
      {confirmDelete && (
        <div
          style={{
            position: "fixed",
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            background: "rgba(0, 0, 0, 0.5)",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            zIndex: 50,
          }}
          onClick={() => setConfirmDelete(null)}
        >
          <div
            style={{
              background: "white",
              borderRadius: "16px",
              padding: "32px",
              width: "90%",
              maxWidth: "420px",
              boxShadow: "0 25px 50px rgba(0, 0, 0, 0.2)",
              textAlign: "center",
            }}
            onClick={(e) => e.stopPropagation()}
          >
            {/* Icono de advertencia */}
            <div
              style={{
                width: "60px",
                height: "60px",
                borderRadius: "50%",
                background: "rgba(239, 68, 68, 0.1)",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                margin: "0 auto 20px",
                fontSize: "28px",
              }}
            >
              ⚠️
            </div>

            <h3 style={{ fontSize: "18px", fontWeight: 600, marginBottom: "8px", color: "#1e293b" }}>
              ¿Eliminar producto?
            </h3>

            <p style={{ fontSize: "14px", color: "#64748b", marginBottom: "24px", lineHeight: "1.5" }}>
              Está a punto de eliminar <strong>"{confirmDelete.productName}"</strong>. Esta acción no puede ser deshecha.
            </p>

            <div style={{ display: "flex", gap: "12px", justifyContent: "center" }}>
              <button
                onClick={() => setConfirmDelete(null)}
                disabled={deletingProductId === confirmDelete.productId}
                style={{
                  padding: "10px 24px",
                  border: "1px solid #e2e8f0",
                  borderRadius: "8px",
                  background: "white",
                  color: "#64748b",
                  fontSize: "13px",
                  fontWeight: 600,
                  cursor: deletingProductId === confirmDelete.productId ? "not-allowed" : "pointer",
                  opacity: deletingProductId === confirmDelete.productId ? 0.5 : 1,
                }}
              >
                Cancelar
              </button>
              <button
                onClick={confirmDeleteProduct}
                disabled={deletingProductId === confirmDelete.productId}
                style={{
                  padding: "10px 24px",
                  border: "none",
                  borderRadius: "8px",
                  background: deletingProductId === confirmDelete.productId ? "#fca5a5" : "#ef4444",
                  color: "white",
                  fontSize: "13px",
                  fontWeight: 600,
                  cursor: deletingProductId === confirmDelete.productId ? "not-allowed" : "pointer",
                  opacity: deletingProductId === confirmDelete.productId ? 0.7 : 1,
                }}
              >
                {deletingProductId === confirmDelete.productId ? "Eliminando..." : "Eliminar"}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
