
  import { createRoot } from "react-dom/client";
  import App from "./app/App.tsx";
  import "./styles/index.css";
  import "./app/lib/debug.ts"; // Cargar utilidades de debug

  createRoot(document.getElementById("root")!).render(<App />);
  