import { ComponentProps, tablePresets } from "@/utils/standardTypes.ts";
import { Button, Card, Input, Typography } from "@material-tailwind/react";
import React, { useEffect, useState } from "react";
import ImagePicker from "@/components/form/ImagePicker.tsx";
import apiRequest from "@/utils/apiRequest.ts";
import Cookies from "js-cookie";
import { useNavigate, useParams } from "react-router-dom";
import fireToast from "@/utils/fireToast.ts";
import Loading from "@/components/Loading.tsx";

export default function StandardTableEditItem({ type }: ComponentProps) {
  const [name, setName] = useState<string>("");
  const [description, setDescription] = useState<string>("");
  const [logo, setLogo] = useState<File | null>(null);
  const [thumbnail, setThumbnail] = useState<File | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const token = Cookies.get("token");

  const { id } = useParams();

  const metadata = tablePresets[type];

  const navigate = useNavigate();

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);

        const res = await apiRequest({
          url: `/api/v1/data/${metadata.pluralName.toLowerCase()}/${id}`,
          method: "GET",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (res.status === 200) {
          const data = res.body;
          setName(data.name);
          setDescription(data.description);
          setLoading(false);
          // Fetch logo
          if (data.logo) {
            const response = await fetch(`/storage/images/logos/${data.logo}`);
            console.info("response:", response);
            const blob = await response.blob();
            const file = new File([blob], "logo.png", { type: blob.type });
            setLogo(file);
          }

          // Fetch thumbnail
          if (data.thumbnail) {
            const response = await fetch(
              `/storage/images/thumbnails/${data.thumbnail}`,
            );
            console.info("response:", response);
            const blob = await response.blob();
            const file = new File([blob], "thumbnail.png", { type: blob.type });
            setThumbnail(file);
          }
        } else {
          console.log(res);
          fireToast(
            "error",
            "An unexpected error has happened, please contact the administrator.",
          );
        }
      } catch (error) {
        console.error("Error fetching files or data:", error);
        fireToast("error", "Failed to load files or data.");
      }
    };

    fetchData();
  }, []);

  const onSubmit = async (e: React.SyntheticEvent) => {
    e.preventDefault();
    const formData = new FormData();
    if (!logo || !thumbnail || !name || !description)
      return fireToast("error", "Please fill all the fields.");

    formData.append("logo", logo);
    formData.append("thumbnail", thumbnail);
    formData.append("name", name);
    formData.append("description", description);

    const res = await apiRequest({
      url: `/api/v1/data/${metadata.pluralName.toLowerCase()}/${id}`,
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
      },
      data: formData,
    });

    console.log(formData);
    console.log(JSON.stringify(formData));

    if (res.status === 200) {
      fireToast("success", `A new ${type} has been successfully modified!`);
      navigate(`/dashboard/${type}`);
    } else {
      console.log(res);
      fireToast(
        "error",
        "An unexpected error has happened, please contact the administrator.",
      );
    }
  };

  if (loading) return <Loading />;

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
              file={logo}
              name={"logo"}
              title={`${metadata.singleName} logo`}
            />
            <ImagePicker
              setFile={setThumbnail}
              file={thumbnail}
              name={"thumbnail"}
              title={`${metadata.singleName} thumbnail`}
            />
          </div>
        </div>
        <Button className="mt-6 w-48" type={"submit"}>
          Save the {metadata.singleName}
        </Button>
      </form>
    </Card>
  );
}
