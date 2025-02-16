import type { Metadata } from "next";
import { haloGrotesk } from "../fonts";

export default function ProjectLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`${haloGrotesk.className}`}>
        {children}
      </body>
    </html>
  );
}
