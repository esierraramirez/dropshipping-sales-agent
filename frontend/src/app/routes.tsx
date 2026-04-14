import { createBrowserRouter, Navigate } from "react-router";
import { DashboardLayout } from "./components/layout/DashboardLayout";
import { LoginPage } from "./pages/auth/LoginPage";
import { RegisterPage } from "./pages/auth/RegisterPage";
import { DashboardPage } from "./pages/DashboardPage";
import { EmpresaPage } from "./pages/EmpresaPage";
import { CatalogoPage } from "./pages/CatalogoPage";
import { AgentePage } from "./pages/AgentePage";
import { OrdenesPage } from "./pages/OrdenesPage";
import { WhatsAppPage } from "./pages/WhatsAppPage";
import { ConfiguracionPage } from "./pages/ConfiguracionPage";

export const router = createBrowserRouter([
  {
    path: "/",
    Component: DashboardLayout,
    children: [
      { index: true, Component: () => <Navigate to="/login" replace /> },
      { path: "dashboard", Component: DashboardPage },
      { path: "empresa", Component: EmpresaPage },
      { path: "catalogo", Component: CatalogoPage },
      { path: "agente", Component: AgentePage },
      { path: "ordenes", Component: OrdenesPage },
      { path: "whatsapp", Component: WhatsAppPage },
      { path: "configuracion", Component: ConfiguracionPage },
    ],
  },
  {
    path: "/login",
    Component: LoginPage,
  },
  {
    path: "/register",
    Component: RegisterPage,
  },
]);
