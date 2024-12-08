import { Outlet } from "react-router-dom";
import Header from "@/layouts/Header.tsx";
import Sidebar from "@/layouts/Sidebar.tsx";
import Footer from "@/layouts/Footer.tsx";

export default function RootLayout() {
  return (
    <main
      className={
        "flex flex-col h-screen w-screen gap-2 bg-base-100 overflow-y-hidden"
      }
    >
      <Header />
      <section className={"flex flex-row gap-2 h-full w-full bg-base-100"}>
        <Sidebar />
        <section
          className={"bg-base-100 w-4/5 h-full flex flex-col justify-between"}
        >
          <div className={"h-full overflow-y-scroll"}>
            <Outlet />
          </div>
          <Footer />
        </section>
      </section>
    </main>
  );
}
