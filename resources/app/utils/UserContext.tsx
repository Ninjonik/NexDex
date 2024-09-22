import React, {
  createContext,
  useContext,
  ReactNode,
  useState,
  useEffect,
} from "react";
import { useLocation, useNavigate } from "react-router-dom";
import Cookies from "js-cookie";
import apiRequest from "@/utils/apiRequest.ts";
import UserInterface from "@/utils/interfaces/UserInterface.ts";

interface UserContextState {
  user: UserInterface | null;
  setUser: React.Dispatch<React.SetStateAction<UserInterface | null>>;
  logoutUser: () => Promise<void>;
}

interface UserContextProps {
  children: ReactNode;
}

const UserContext = createContext<UserContextState | undefined>(undefined);

export const useUserContext = () => {
  const context = useContext(UserContext);
  if (!context) {
    throw new Error("useUserContext must be used within a UserContextProvider");
  }
  return context;
};

export const UserContextProvider = ({ children }: UserContextProps) => {
  const [user, setUser] = useState<UserInterface | null>(null);
  const navigate = useNavigate();
  const currentRoute = useLocation();
  const currentPage = currentRoute.pathname;

  const logoutUser = async () => {
    try {
      localStorage.removeItem("user");
      Cookies.remove("token");
      setUser(null);
    } catch (error) {
      /* empty */
    }
  };

  // Check if user is logged in
  useEffect(() => {
    const token = Cookies.get("token");
    if (!token && !currentPage.includes("login")) navigate("/login");

    // Get user data
    const getUserData = async () => {
      try {
        const response = await apiRequest({
          url: "/api/v1/auth/user",
          method: "GET",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (response.status === 200) {
          setUser(response.body.user);
        } else {
          setUser(null);
          navigate("/login");
        }
      } catch (error) {
        console.error("Error fetching user data:", error);
        setUser(null);
        navigate("/login");
      }
    };

    if (token) {
      getUserData();
    }
  }, []);

  return (
    <UserContext.Provider value={{ user, setUser, logoutUser }}>
      {children}
    </UserContext.Provider>
  );
};
