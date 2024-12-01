import React from "react";
import { Route, Routes } from "react-router-dom";
import RootLayout from "@/layouts/RootLayout";
import RouteLoading from "@/components/RouteLoading";
import Error404 from "@/components/404";
import StandardTableView from "@/components/StandardTableView";
import StandardTableAddItem from "@/components/StandardTableAddItem";

const Home = React.lazy(() => import("@/pages/Home"));
const Login = React.lazy(() => import("@/pages/Login"));

// Define types for components
type AllowedRouteNames =
  | "factions"
  | "ideologies"
  | "abilities"
  | "economies"
  | "regimes"
  | "countryballs";

// Array of route definitions
const routes: {
  name: AllowedRouteNames;
  component: typeof StandardTableView;
}[] = [
  { name: "factions", component: StandardTableView },
  { name: "ideologies", component: StandardTableView },
  { name: "abilities", component: StandardTableView },
  { name: "economies", component: StandardTableView },
  { name: "regimes", component: StandardTableView },
  { name: "countryballs", component: StandardTableView },
];

const RoutesList: React.FC = () => {
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
        {routes.map((route) => (
          <>
            <Route
              path={route.name}
              element={<StandardTableView type={route.name} />}
              key={route.name + "_std"}
            />
            <Route
              path={`${route.name}/add`}
              element={<StandardTableAddItem type={route.name} />}
              key={route.name + "_add"}
            />
          </>
        ))}
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
