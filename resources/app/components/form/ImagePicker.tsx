import { Typography } from "@material-tailwind/react";
import { ChangeEvent, Dispatch, SetStateAction, useState } from "react";

interface ComponentProps {
  setFile: Dispatch<SetStateAction<File | null>>;
  name: string;
  title: string;
}

const ImagePicker = ({ setFile, name, title }: ComponentProps) => {
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);

  const generatePreviewUrl = (file: File): string | null => {
    if (!file.type || !file.type.startsWith("image/")) {
      return null;
    }

    if (file.type === "image/svg+xml") {
      // For SVG, we can use the URL.createObjectURL()
      return URL.createObjectURL(file);
    } else {
      // For other image formats, we create a FileReader object
      const reader = new FileReader();
      reader.onload = () => {
        setPreviewUrl(reader.result as string);
      };
      reader.readAsDataURL(file);
      return "";
    }
  };

  const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file && file.type.match("image.*")) {
      setFile(file);
      generatePreviewUrl(file);
    } else {
      setFile(null);
      setPreviewUrl(null);
    }
  };

  return (
    <div className={"flex flex-col gap-6"}>
      <Typography variant="h6" color="blue-gray" className="-mb-3">
        Upload {title}
      </Typography>
      <div>
        <input
          className="file:bg-primary file:p-2 border-blue-gray-200 file:shadow-none file:border-0 border-none block w-full text-sm text-gray-900 border rounded-lg cursor-pointer dark:text-gray-400 focus:outline-none dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400"
          id={name}
          name={name}
          type="file"
          accept=".svg,.png,.jpg,.gif"
          onChange={handleFileChange}
        />
        <div
          className="mt-1 text-sm text-gray-500 dark:text-gray-300"
          id="file_input_help"
        >
          SVG, PNG, JPG
        </div>
        {previewUrl && (
          <img src={previewUrl} alt="Uploaded Image Preview" className="w-48" />
        )}
      </div>
    </div>
  );
};

export default ImagePicker;
