"use client";
import React from "react";
import { FunctionSquare, Instagram, MailIcon, Twitter } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useRouter } from "next/navigation";
import { gothicFont, haloGrotesk, inter } from "@/app/fonts";

const Footer = () => {
    const router = useRouter();
    return (
        <footer
            className={`${haloGrotesk.className} bg-transparent text-white pb-9 px-10 md:px-80`}
        >
            <div className="container mx-auto flex tracking-wide flex-col md:flex-row gap-y-4 justify-between pt-10 pb-14 items-start">
                <div className="flex flex-col items-start gap-y-2">
                    <div className="flex items-center gap-x-2">
                        <h2 className="text-xl text-white">Runway</h2>
                    </div>

                    <p className="w-[300px] text-gray-300 tracking-wide text-xs">
                        <span className={inter.className}>©</span> 2025 Runway<br/><br/>Built with ❤️ at TreeHacks 2025

                        <br/>by the team at:<br/>
                        <a href="https://opennote.me" target="_blank">
                            <img src="/opennotebanner.png" alt="Opennote Logo" className="w-36 inline-block" />
                        </a>
                    </p>
                    <div className="flex flex-col gap-y-2 mt-4">
                        <div className="flex flex-row items-start gap-x-6">
                        </div>
                    </div>
                </div>

                <div className="grid grid-cols-1">
                    <div className="flex flex-col gap-y-0 items-start justify-start">
                        {/* <Button
                            onClick={() => router.push("/info/help")}
                            variant="link"
                            className="text-white hover:text-gray-300"
                        >
                            Help
                        </Button> */}
                        <Button
                            onClick={() => router.push("/project")}
                            variant="link"
                            className="text-white hover:text-gray-300"
                        >
                            Start Building
                        </Button>
                        {/* <Button
                            onClick={() => router.push("/info/toc")}
                            variant="link"
                            className="text-white hover:text-gray-300"
                        >
                            Terms of Service
                        </Button>
                        <Button
                            onClick={() => router.push("/info/privacy-policy")}
                            variant="link"
                            className="text-white hover:text-gray-300"
                        >
                            Privacy Policy
                        </Button> */}
                    </div>
                </div>
            </div>
        </footer>
    );
};

export default Footer;
