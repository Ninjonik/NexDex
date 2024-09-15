import { FaFileAlt, FaUser, FaShoppingCart, FaCog } from "react-icons/fa";
import { FaRocket } from "react-icons/fa6";

const Sidebar = () => {
  return (
    <aside className={"bg-base-100 w-[15%] h-full px-2 flex flex-col gap-2"}>
      <ul className="pb-2 pt-1">
        <li>
          <a
            href="https://demos.creative-tim.com/soft-ui-flowbite-pro/mailing/inbox/"
            target="_blank"
            className="flex items-center py-2.5 px-4 text-base font-normal text-dark-500 rounded-lg hover:bg-gray-200 group transition-all duration-200"
            data-ripple-light="true"
          >
            <span
              className={
                "bg-base-200 p-2 rounded-md flex justify-center items-center text-center"
              }
            >
              <FaFileAlt />
            </span>
            <span className="ml-3 text-dark-500 text-sm font-light">
              Kanban
            </span>
          </a>
        </li>
        <li>
          <a
            href="https://demos.creative-tim.com/soft-ui-flowbite/kanban/"
            target="_blank"
            className="flex items-center py-2.5 px-4 text-base font-normal text-dark-500 rounded-lg hover:bg-gray-200 group transition-all duration-200"
          >
            <span
              className={
                "bg-base-200 p-2 rounded-md flex justify-center items-center text-center"
              }
            >
              <FaUser />
            </span>
            <span className="ml-3 text-dark-500 text-sm font-light">Inbox</span>
          </a>
        </li>
        <li>
          <a
            href="https://demos.creative-tim.com/soft-ui-flowbite/users"
            className="flex items-center py-2.5 px-4 text-base font-normal text-dark-500 rounded-lg hover:bg-gray-200  group transition-all duration-200"
          >
            <span
              className={
                "bg-base-200 p-2 rounded-md flex justify-center items-center text-center"
              }
            >
              <FaUser />
            </span>
            <span className="ml-3 text-dark-500 text-sm font-light">Users</span>
          </a>
        </li>
        <li>
          <a
            href="https://demos.creative-tim.com/soft-ui-flowbite/products"
            className="flex items-center py-2.5 px-4 text-base font-normal text-dark-500 rounded-lg hover:bg-gray-200  group transition-all duration-200"
          >
            <span
              className={
                "bg-base-200 p-2 rounded-md flex justify-center items-center text-center"
              }
            >
              <FaShoppingCart />
            </span>
            <span className="ml-3 text-dark-500 text-sm font-light">
              Products
            </span>
          </a>
        </li>
        <li>
          <a
            href="https://demos.creative-tim.com/soft-ui-flowbite/sign-in"
            className="flex items-center py-2.5 px-4 text-base font-normal text-dark-500 rounded-lg hover:bg-gray-200 group transition-all duration-200"
          >
            <span
              className={
                "bg-base-200 p-2 rounded-md flex justify-center items-center text-center"
              }
            >
              <FaRocket />
            </span>
            <span className="ml-3 text-dark-500 text-sm font-light">
              Sign In
            </span>
          </a>
        </li>
        <li>
          <a
            href="https://demos.creative-tim.com/soft-ui-flowbite/sign-up"
            className="flex items-center py-2.5 px-4 text-base font-normal text-dark-500 rounded-lg hover:bg-gray-200 group transition-all duration-200"
          >
            <span
              className={
                "bg-base-200 p-2 rounded-md flex justify-center items-center text-center"
              }
            >
              <FaCog />
            </span>
            <span className="ml-3 text-dark-500 text-sm font-light">
              Sign Up
            </span>
          </a>
        </li>
      </ul>
    </aside>
  );
};

export default Sidebar;
