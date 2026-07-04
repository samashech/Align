import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: "export",
  devIndicators: false,
  // @ts-ignore
  turbopack: {
    root: __dirname,
  },
};

export default nextConfig;
