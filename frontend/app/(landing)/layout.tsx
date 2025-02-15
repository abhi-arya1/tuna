"use client";

import Navbar from "./_components/navbar";
import Footer from "./_components/footer";


const LandingLayout = ({ children }: { children: React.ReactNode }) => {
    return (
            <main className="flex-1 h-full w-screen overflow-x-clip">
                <Navbar />
                {children}
                <Footer />
            </main>
    );
};

export default LandingLayout;
