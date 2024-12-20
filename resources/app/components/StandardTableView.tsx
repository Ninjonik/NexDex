import { UserPlusIcon } from "@heroicons/react/24/solid";
import {
  Avatar,
  Button,
  Card,
  CardBody,
  CardFooter,
  CardHeader,
  IconButton,
  Tab,
  Tabs,
  TabsHeader,
  Typography,
} from "@material-tailwind/react";
import { ComponentProps, tablePresets } from "@/utils/standardTypes.ts";
import { Link, useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import apiRequest from "@/utils/apiRequest.ts";
import Cookies from "js-cookie";
import fireToast from "@/utils/fireToast.ts";
import Loading from "@/components/Loading.tsx";
import { PencilIcon, TrashIcon } from "@heroicons/react/16/solid";

export default function StandardTableView({ type }: ComponentProps) {
  const metadata = tablePresets[type];
  const token = Cookies.get("token");

  const [data, setData] = useState<any[] | []>([]);
  const [loading, setLoading] = useState<boolean>(true);
  useEffect(() => {
    const fetchData = async () => {
      const res = await apiRequest({
        url: `/api/v1/data/${metadata.pluralName.toLowerCase()}`,
        method: "GET",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (res.status === 200) {
        setData(res.body);
      } else {
        console.log(res);
        fireToast(
          "error",
          "An unexpected error has happened, please contact the administrator.",
        );
      }
      setLoading(false);
    };

    setData([]);
    setLoading(true);
    fetchData();
  }, [type, metadata]);

  const handleDeleteAction = async (id: number) => {
    const res = await apiRequest({
      url: `/api/v1/data/${metadata.pluralName.toLowerCase()}/${id}`,
      method: "DELETE",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    if (res.status === 200) {
      fireToast("success", `Table row has been successfully deleted!`);
      setData((prevData) => {
        return prevData.filter((item) => item.id !== id);
      });
    } else {
      console.log(res);
      fireToast(
        "error",
        "An unexpected error has happened, please contact the administrator.",
      );
    }
  };

  const navigate = useNavigate();

  return (
    <Card className="h-full w-full bg-base-100 shadow-none">
      <CardHeader
        floated={false}
        shadow={false}
        className="rounded-none bg-base-100"
      >
        <div className="mb-8 flex items-center justify-between gap-8">
          <div>
            <Typography variant="h5" color="blue-gray">
              {metadata.pluralName} list
            </Typography>
            <Typography color="gray" className="mt-1 font-normal">
              See information about all {metadata.pluralName}
            </Typography>
          </div>
          <div className="flex shrink-0 flex-col gap-2 sm:flex-row">
            <Button variant="outlined" size="sm">
              view all
            </Button>
            <Link to={`/dashboard/${type}/add`}>
              <Button className="flex items-center gap-3" size="sm">
                <UserPlusIcon strokeWidth={2} className="h-4 w-4" /> Add{" "}
                {metadata.singleName}
              </Button>
            </Link>
          </div>
        </div>
        <div className="flex flex-col items-center justify-between gap-4 md:flex-row w-full">
          {Object.keys(metadata.tabs).length > 0 && (
            <Tabs value="all" className="w-full md:w-max">
              <TabsHeader>
                {metadata.tabs.map(({ label, value }) => (
                  <Tab key={value} value={value}>
                    &nbsp;&nbsp;{label}&nbsp;&nbsp;
                  </Tab>
                ))}
              </TabsHeader>
            </Tabs>
          )}
          {/*<div className="w-full md:w-72">*/}
          {/*  <Input*/}
          {/*    label="Search"*/}
          {/*    icon={<MagnifyingGlassIcon className="h-5 w-5" />}*/}
          {/*    crossOrigin={undefined}*/}
          {/*  />*/}
          {/*</div>*/}
        </div>
      </CardHeader>
      <CardBody className="overflow-y-scroll px-0">
        {data && data.length > 0 ? (
          <table className="mt-4 w-full min-w-max table-auto text-left">
            <thead>
              <tr>
                <th className="cursor-pointer border-y border-blue-gray-100 bg-blue-gray-50/50 p-4 transition-colors hover:bg-blue-gray-50">
                  <Typography
                    variant="small"
                    color="blue-gray"
                    className="flex items-center justify-between gap-2 font-normal leading-none opacity-70"
                  >
                    Actions
                  </Typography>
                </th>
                {Object.keys(data[0]).map((key, index) => (
                  <th
                    key={index + key + "_table_header"}
                    className="cursor-pointer border-y border-blue-gray-100 bg-blue-gray-50/50 p-4 transition-colors hover:bg-blue-gray-50"
                  >
                    <Typography
                      variant="small"
                      color="blue-gray"
                      className="flex items-center justify-between gap-2 font-normal leading-none opacity-70"
                    >
                      {key.toUpperCase()}
                    </Typography>
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {data.map((record, index) => (
                <tr key={record.id + index + "_table_record"}>
                  <td
                    key={record.id + index + "_table_record_" + -1 + "actions"}
                    className={"p-4"}
                  >
                    <div className="flex items-center gap-2">
                      <IconButton
                        variant="text"
                        size="sm"
                        onClick={() =>
                          navigate(`/dashboard/${type}/edit/${record.id}`)
                        }
                      >
                        <PencilIcon className="h-4 w-4 text-gray-900" />
                      </IconButton>
                      <IconButton
                        variant="text"
                        size="sm"
                        onClick={() => handleDeleteAction(record.id)}
                      >
                        <TrashIcon
                          strokeWidth={3}
                          className="h-4 w-4 text-gray-900"
                        />
                      </IconButton>
                    </div>
                  </td>
                  {Object.entries(record).map(([key, value], i) => (
                    <td
                      key={record.id + index + "_table_record_" + i + key}
                      className={"p-4"}
                    >
                      {key === "logo" || key === "thumbnail" ? (
                        <div className="">
                          <Avatar
                            src={`/storage/images/${key}s/${value}`}
                            alt={key}
                            size="sm"
                          />
                        </div>
                      ) : (
                        <div className="">
                          <Typography
                            variant="small"
                            color="blue-gray"
                            className="font-normal"
                          >
                            {value as string}
                          </Typography>
                        </div>
                      )}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          !loading && (
            <span
              className={
                "text-center font-bold w-full flex justify-center items-center"
              }
            >
              No data has been found.
            </span>
          )
        )}
        {loading && <Loading />}
      </CardBody>
      <CardFooter className="flex items-center justify-between border-t border-blue-gray-50 p-4">
        <Typography variant="small" color="blue-gray" className="font-normal">
          Page 1 of 10
        </Typography>
        <div className="flex gap-2">
          <Button variant="outlined" size="sm">
            Previous
          </Button>
          <Button variant="outlined" size="sm">
            Next
          </Button>
        </div>
      </CardFooter>
    </Card>
  );
}
