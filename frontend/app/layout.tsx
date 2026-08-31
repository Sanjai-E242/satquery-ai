import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'SATQUERY AI — Interactive Agentic Remote-Sensing VLM',
  description: 'Multimodal Remote-Sensing Vision-Language Assistant for SIH and ISRO Geospatial Intelligence',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className="bg-space-950 text-slate-100 font-sans min-h-screen">
        {children}
      </body>
    </html>
  );
}
