import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import "@/styles/index.scss";
import { ThemeProvider } from "@material-tailwind/react";

ReactDOM.createRoot(document.getElementById("root") as HTMLElement).render(
  <React.StrictMode>
    <ThemeProvider>
      <App />
    </ThemeProvider>
  </React.StrictMode>,
);

// console.log(import.meta.env.VITE_APP_URL);
