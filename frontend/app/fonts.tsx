import localFont from "next/font/local"
import { Inter } from "next/font/google"

export const inter = Inter({ subsets: ["latin"] });

export const gothicFont = localFont({
    src: "./fonts/Gothic60-Regular.ttf",
    display: "swap",
  });

export const haloGrotesk = localFont({
    src: "./fonts/HaloGrotesk-Regular.ttf",
    display: "swap",
  });
