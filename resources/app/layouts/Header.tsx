import { Link } from "react-router-dom";
import { Button, IconButton } from "@material-tailwind/react";
import { FaGithub } from "react-icons/fa6";

export default function Header() {
  return (
    <header
      className={
        "h-[7.5%] w-full flex flex-row justify-between gap-2 p-2 px-4 bg-base-100"
      }
    >
      <h1
        className={
          "text-3xl flex text-center justify-center items-center font-semibold"
        }
      >
        NexDex
      </h1>
      <nav className={"flex items-center justify-center"}>
        <Link to="" className="mr-4 text-lg font-medium">
          <Button className={"bg-gradient-to-r from-red-500 to-purple-500"}>
            Support us
          </Button>
        </Link>
        <Link
          to="https://github.com/ninjonik/nexdex"
          className="mr-4 text-lg font-medium"
        >
          <IconButton>
            <FaGithub />
          </IconButton>
        </Link>
      </nav>
    </header>
  );
}
