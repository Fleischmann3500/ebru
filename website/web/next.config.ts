import type { NextConfig } from 'next';

const nextConfig: NextConfig = {
  // Bilder aus Sanity laufen über den eigenen Bild-Optimierer: Besucher verbinden sich nicht mit Sanity.
  images: { remotePatterns: [{ protocol: 'https', hostname: 'cdn.sanity.io' }], formats: ['image/avif', 'image/webp'] },
  async headers() {
    return [{ source: '/welt/:path*', headers: [{ key: 'Cache-Control', value: 'public, max-age=31536000, immutable' }] }];
  },
};
export default nextConfig;
