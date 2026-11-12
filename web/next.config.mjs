/** Static export: the whole site is prebuilt from the pipeline's JSON files. */
const nextConfig = {
  output: "export",
  trailingSlash: true,
  images: { unoptimized: true },
};
export default nextConfig;
