import type { Metadata } from "next";
import { IBM_Plex_Sans } from "next/font/google";
import "./globals.css";
import { Navbar } from "@/components/Navbar";

// Load IBM Plex Sans (The official IBM font)
const ibmPlex = IBM_Plex_Sans({
  subsets: ["latin"],
  weight: ["400", "500", "600", "700"],
  variable: "--font-ibm-plex",
});

export const metadata: Metadata = {
  title: "RepoPilot | AI Developer Onboarding",
  description: "Turn any GitHub repository into a guided, interactive onboarding tour powered by IBM Bob 2.0.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className={ibmPlex.variable}>
      <body className="font-sans antialiased bg-gray-50 text-gray-900">
        <Navbar />
        <main className="min-h-[calc(100vh-4rem)]">
          {children}
        </main>
      </body>
    </html>
  );
}