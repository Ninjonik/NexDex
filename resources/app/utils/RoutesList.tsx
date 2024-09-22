import React from "react";
import { Route, Routes } from "react-router-dom";
import RootLayout from "@/layouts/RootLayout.tsx";
import RouteLoading from "@/components/RouteLoading.tsx";
import Error404 from "@/components/404.tsx";

const Home = React.lazy(() => import("@/pages/Home.tsx"));
const Login = React.lazy(() => import("@/pages/Login.tsx"));

const RoutesList = () => {
  return (
    <Routes>
      <Route path="/dashboard" element={<RootLayout />}>
        <Route
          index
          element={
            <React.Suspense fallback={<RouteLoading />}>
              <Home />
            </React.Suspense>
          }
        />
        <Route path="*" element={<Error404 />} />
      </Route>
      <Route
        path="/login"
        element={
          <React.Suspense fallback={<RouteLoading />}>
            <Login />
          </React.Suspense>
        }
      />
    </Routes>
  );
};

export default RoutesList;
