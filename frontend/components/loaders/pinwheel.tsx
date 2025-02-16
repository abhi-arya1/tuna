"use client";

import { useEffect } from 'react'

export default function PinwheelLoader(
    { className = "", color = "gray", size = "45", speed = "1.4" }:
    { className?: string; color?: string, size?: string, speed?: string }
) {
    useEffect(() => {
        async function getLoader() {
        const { pinwheel } = await import('ldrs')
            pinwheel.register()
        }
        getLoader()
    }, [])
    return (
        <div className={className}>
            <l-pinwheel
                color={color}
                size={size}
                speed={speed}
            ></l-pinwheel>
        </div>
    )
}
