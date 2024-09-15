import withMT from "@material-tailwind/react/utils/withMT";

export default withMT({
  content: [
    "./resources/views/app.blade.php",
    "./resources/app/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      zIndex: {
        1000: "1000",
        2000: "2000",
        5000: "5000",
        5050: "5050",
      },
      colors: {
        "color-scheme": "light",
        default: "#FFFFFF",
        primary: "#49B6FF",
        secondary: "oklch(69.71% 0.329 342.55)",
        "secondary-content": "oklch(98.71% 0.0106 342.55)",
        accent: "oklch(76.76% 0.184 183.61)",
        neutral: "#f4f5f7",
        "neutral-content": "#2a323c",
        "base-300": "#F3F3F3",
        "base-200": "#E8E8E8",
        "base-100": "#E0E0E0",
        "base-content": "#1f2937",
        danger: "#e53e3e",
        success: "#48bb78",
        warning: "#f59e0b",
        info: "#3182ce",
      },
    },
  },
  plugins: [],
});
