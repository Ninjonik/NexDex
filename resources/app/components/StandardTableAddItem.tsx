import { ComponentProps, tablePresets } from "@/utils/standardTypes.ts";
import { Button, Card, Input, Typography } from "@material-tailwind/react";
import React, { useState } from "react";
import ImagePicker from "@/components/form/ImagePicker.tsx";
import apiRequest from "@/utils/apiRequest.ts";
import Cookies from "js-cookie";
import { useNavigate } from "react-router-dom";

export default function StandardTableAddItem({ type }: ComponentProps) {
  const [name, setName] = useState<string>("");
  const [description, setDescription] = useState<string>("");
  const [logo, setLogo] = useState<File | null>(null);
  const [thumbnail, setThumbnail] = useState<File | null>(null);
  const token = Cookies.get("token");

  const metadata = tablePresets[type];

  const navigate = useNavigate();

  const onSubmit = async (e: React.SyntheticEvent) => {
    e.preventDefault();
    const formData = new FormData();
    if (!logo || !thumbnail) return;

    formData.append("logo", logo);
    formData.append("thumbnail", thumbnail);
    formData.append("name", name);
    formData.append("description", description);

    const res = await apiRequest({
      url: `/api/v1/data/${metadata.pluralName.toLowerCase()}`,
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
      },
      data: formData,
    });

    if (res.status === 200) {
      navigate(`/dashboard/${type}`);
    } else {
      console.log(res);
      // Fire error toast
    }
  };

  return (
    <Card color="transparent" shadow={false} className={"gap-4"}>
      <Typography variant="h4" color="blue-gray">
        Add a {metadata.singleName}
      </Typography>
      {/*
      <Typography color="gray" className="mt-1 font-normal">
        Nice to meet you! Enter your details to register.
      </Typography>
      */}
      <form
        className={"flex flex-col gap-2 justify-between h-full"}
        onSubmit={onSubmit}
      >
        <div className="flex flex-row gap-2 w-full">
          <div className="mb-1 flex flex-col gap-6 w-1/2">
            <Typography variant="h6" color="blue-gray" className="-mb-3">
              Name
            </Typography>
            <Input
              size="lg"
              placeholder="Name"
              className=" !border-t-blue-gray-200 focus:!border-t-gray-900"
              crossOrigin={undefined}
              name={"name"}
              variant={"outlined"}
              value={name}
              type={"text"}
              onChange={(e) => setName(e.target.value)}
            />
            <Typography variant="h6" color="blue-gray" className="-mb-3">
              Description
            </Typography>
            <Input
              size="lg"
              placeholder="Description"
              className=" !border-t-blue-gray-200 focus:!border-t-gray-900"
              crossOrigin={undefined}
              name={"description"}
              variant={"outlined"}
              value={description}
              type={"text"}
              onChange={(e) => setDescription(e.target.value)}
            />
          </div>
          <div className={"flex flex-col gap-2 w-1/2"}>
            <ImagePicker
              setFile={setLogo}
              name={"logo"}
              title={`${metadata.singleName} logo`}
            />
            <ImagePicker
              setFile={setThumbnail}
              name={"thumbnail"}
              title={`${metadata.singleName} thumbnail`}
            />
          </div>
        </div>
        <Button className="mt-6 w-48" type={"submit"}>
          Create a new {metadata.singleName}
        </Button>
      </form>
    </Card>
  );
}
