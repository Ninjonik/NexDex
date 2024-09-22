import { useEffect, useRef } from "react";

export default function CurrentDateTime() {
  const dateTimeRef = useRef<HTMLSpanElement>(null);

  useEffect(() => {
    const secondsTimer = setInterval(() => {
      if (dateTimeRef.current) {
        dateTimeRef.current.innerText = new Date().toLocaleString();
      }
    }, 1000);
    return () => clearInterval(secondsTimer);
  }, []);

  return <span ref={dateTimeRef} />;
}
