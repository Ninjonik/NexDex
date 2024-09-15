import {
  Card,
  Button,
  CardBody,
  CardHeader,
  Typography,
} from "@material-tailwind/react";
import WebCard from "@/components/WebCard.tsx";

const data = [
  {
    cardNum: "#1",
    profileImg: "https://www.material-tailwind.com/img/avatar1.jpg",
    name: "Tina Andrew",
    desc: "Creator",
    imgs: [
      "/image/web3-card-1.svg",
      "/image/web3-card-2.svg",
      "/image/web3-card-3.svg",
    ],
  },
  {
    cardNum: "#2",
    profileImg: "https://www.material-tailwind.com/image/avatar2.jpg",
    name: "Linde Michael",
    desc: "Creator",
    imgs: [
      "/image/web3-card-5-mini.svg",
      "/image/web3-card-6-mini.svg",
      "/image/web3-card-7-mini.svg",
    ],
  },
  {
    cardNum: "#3",
    profileImg: "https://www.material-tailwind.com/image/avatar7.svg",
    name: "Misha Stam",
    desc: "Creator",
    imgs: [
      "/image/web3-card-4.svg",
      "/image/web3-card-4.svg",
      "/image/web3-card-4.svg",
    ],
  },
];

function Home() {
  return (
    <section className="px-8 py-10">
      <Card shadow={false} className="border border-gray-300">
        <CardHeader
          shadow={false}
          floated={false}
          className="flex overflow-visible gap-y-4 flex-wrap items-start justify-between rounded-none"
        >
          <div>
            <Typography
              color="blue-gray"
              variant="h1"
              className="!text-2xl mb-1"
            >
              Top Creators
            </Typography>
            <Typography
              color="blue-gray"
              className="!text-lg font-normal text-gray-600"
            >
              The most sought-after collections across the entire ecosystem.
            </Typography>
          </div>
          <div className="flex shrink-0 gap-2">
            <Button size="sm" variant="outlined" className="border-gray-300">
              Last 24h
            </Button>
            <Button size="sm" variant="outlined" className="border-gray-300">
              Last week
            </Button>
            <Button size="sm" variant="outlined">
              Last month
            </Button>
          </div>
        </CardHeader>
        <CardBody className="grid xl:grid-cols-3 grid-cols-1 gap-4 px-4">
          {data.map((props, key) => (
            <WebCard key={key} {...props} />
          ))}
        </CardBody>
      </Card>
    </section>
  );
}

export default Home;
