import ToastNotifications from "@/components/ToastNotifications";
import { BrowserRouter } from "react-router-dom";
import { UserContextProvider } from "@/utils/UserContext.tsx";
import RoutesList from "@/utils/RoutesList.tsx";

function App() {
  return (
    <BrowserRouter>
      <div className="block relative">
        <ToastNotifications />
      </div>
      <UserContextProvider>
        <RoutesList />
      </UserContextProvider>
    </BrowserRouter>
  );
}

export default App;
