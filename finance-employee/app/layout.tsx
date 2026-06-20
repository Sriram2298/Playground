import type { Metadata } from "next";
import { Geist } from "next/font/google";
import "./globals.css";
import Sidebar from "@/components/Sidebar";
import DemoBanner from "@/components/DemoBanner";

const geist = Geist({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Finance Agent – Zamp",
  description: "Autonomous AP/AR digital employee",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className="h-full">
      <body className={`${geist.className} bg-gray-50 h-full`}>
        <DemoBanner />
        <div className="flex" style={{ height: "calc(100vh - 32px)" }}>
          <Sidebar />
          <main className="flex-1 overflow-y-auto">{children}</main>
        </div>
      </body>
    </html>
  );
}
