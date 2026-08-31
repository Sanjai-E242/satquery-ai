/** @type {import('next').NextConfig} */
const backendUrl = (
  process.env.BACKEND_API_URL || 
  process.env.NEXT_PUBLIC_API_URL || 
  'http://127.0.0.1:8000'
).replace(/\/$/, '');

const nextConfig = {
  reactStrictMode: true,
  images: {
    unoptimized: true,
  },
  async rewrites() {
    return [
      {
        source: '/storage/:path*',
        destination: `${backendUrl}/storage/:path*`,
      },
      {
        source: '/media/:path*',
        destination: `${backendUrl}/media/:path*`,
      },
    ];
  },
};

module.exports = nextConfig;
