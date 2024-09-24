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

interface TableRouteProps {
  type: AllowedRouteNames;
}

const TableRoute: React.FC<TableRouteProps> = ({ type }) => (
  <>
    <Route path={type} element={<StandardTableView type={type} />} />
    <Route
      path={`${type}/add`}
      element={<StandardTableAddItem type={type} />}
    />
  </>
);

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
          <TableRoute key={route.name} type={route.name} />
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
