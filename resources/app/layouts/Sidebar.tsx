import {
  Accordion,
  AccordionBody,
  AccordionHeader,
  Card,
  List,
  ListItem,
  ListItemPrefix,
  Typography,
} from "@material-tailwind/react";
import {
  ChevronDownIcon,
  ChevronRightIcon,
  Cog6ToothIcon,
  PowerIcon,
  PresentationChartBarIcon,
} from "@heroicons/react/24/solid";
import { useState } from "react";
import { Link } from "react-router-dom";
import { useUserContext } from "@/utils/UserContext.tsx";
import GuildInterface from "@/utils/interfaces/GuildInterface.ts";
import {
  FaCoins,
  FaFlag,
  FaHandshake,
  FaServer,
  FaStamp,
  FaStar,
} from "react-icons/fa6";
import { MdBallot } from "react-icons/md";
import { VscGraph } from "react-icons/vsc";

export default function Sidebar() {
  const { user } = useUserContext();

  const [open, setOpen] = useState(0);

  const handleOpen = (value: number) => {
    setOpen(open === value ? 0 : value);
  };

  if (!user) return;

  const guildsData = JSON.parse(user.discord_guilds) as GuildInterface[];

  return (
    <Card className="w-1/5 p-4 bg-base-100 shadow-none overflow-y-auto">
      <span className={""}>Welcome, {user.name}</span>
      <List>
        <Link to={"/dashboard"}>
          <ListItem>
            <ListItemPrefix>
              <PresentationChartBarIcon className="h-5 w-5" />
            </ListItemPrefix>
            Dashboard
          </ListItem>
        </Link>
        <Link to={"/dashboard/stats"}>
          <ListItem>
            <ListItemPrefix>
              <VscGraph className={"h-5 w-5"} />
            </ListItemPrefix>
            Stats
          </ListItem>
        </Link>
        <Link to={"/dashboard/countryballs"}>
          <ListItem>
            <ListItemPrefix>
              <FaFlag className={"h-5 w-5"} />
            </ListItemPrefix>
            Countryballs
          </ListItem>
        </Link>
        <Link to={"/dashboard/abilities"}>
          <ListItem>
            <ListItemPrefix>
              <FaStar className={"h-5 w-5"} />
            </ListItemPrefix>
            Ability Types
          </ListItem>
        </Link>
        <Link to={"/dashboard/economies"}>
          <ListItem>
            <ListItemPrefix>
              <FaCoins className={"h-5 w-5"} />
            </ListItemPrefix>
            Economy
          </ListItem>
        </Link>
        <Link to={"/dashboard/regimes"}>
          <ListItem>
            <ListItemPrefix>
              <MdBallot className={"h-5 w-5"} />
            </ListItemPrefix>
            Regimes
          </ListItem>
        </Link>
        <Link to={"/dashboard/ideologies"}>
          <ListItem>
            <ListItemPrefix>
              <FaStamp className={"h-5 w-5"} />
            </ListItemPrefix>
            Ideology
          </ListItem>
        </Link>
        <Link to={"/dashboard/factions"}>
          <ListItem>
            <ListItemPrefix>
              <FaHandshake className={"h-5 w-5"} />
            </ListItemPrefix>
            Factions/Alliances
          </ListItem>
        </Link>
        <hr className="my-2 border-blue-gray-50" />
        <Accordion
          open={open === 1}
          icon={
            <ChevronDownIcon
              strokeWidth={2.5}
              className={`mx-auto h-4 w-4 transition-transform ${open === 1 ? "rotate-180" : ""}`}
            />
          }
        >
          <ListItem className="p-0" selected={open === 1}>
            <AccordionHeader
              onClick={() => handleOpen(1)}
              className="border-b-0 p-3"
            >
              <ListItemPrefix>
                <FaServer className="h-5 w-5" />
              </ListItemPrefix>
              <Typography color="blue-gray" className="mr-auto font-normal">
                My servers
              </Typography>
            </AccordionHeader>
          </ListItem>
          <AccordionBody className="py-1">
            <List className="p-0">
              {user.discord_guilds &&
                Object.keys(guildsData).length > 0 &&
                Object.entries(guildsData).map(([guildId, guild]) => (
                  <ListItem key={"sidebar_" + guildId}>
                    <ListItemPrefix>
                      <ChevronRightIcon strokeWidth={3} className="h-3 w-5" />
                    </ListItemPrefix>
                    {guild.name}
                  </ListItem>
                ))}
            </List>
          </AccordionBody>
        </Accordion>
        <hr className="my-2 border-blue-gray-50" />
        <ListItem>
          <ListItemPrefix>
            <Cog6ToothIcon className="h-5 w-5" />
          </ListItemPrefix>
          Settings
        </ListItem>
        <Link to={"/logout"}>
          <ListItem>
            <ListItemPrefix>
              <PowerIcon className="h-5 w-5" />
            </ListItemPrefix>
            Log Out
          </ListItem>
        </Link>
      </List>
    </Card>
  );
}
