import { Spinner } from "@material-tailwind/react";

const Loading = () => {
  return (
    <div className={"w-full h-full flex justify-center items-center text-4xl"}>
      <Spinner />
    </div>
  );
};

export default Loading;
