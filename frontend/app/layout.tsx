import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

import { gothicFont, haloGrotesk } from "./fonts";


export const metadata: Metadata = {
  title: "Runway",
  description: "The Vercel for AI Models",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${haloGrotesk.className} antialiased`}
      >
        {children}
      </body>
    </html>
  );
}
