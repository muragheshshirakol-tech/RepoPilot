"use client";

import Link from "next/link";
import { Rocket, Code, Zap } from "lucide-react"; // Changed Github to Code

export function Navbar() {
    return (
        <nav className="border-b bg-white/80 backdrop-blur-md sticky top-0 z-50 shadow-sm">
            <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
                {/* Logo */}
                <Link href="/" className="flex items-center gap-2 font-bold text-lg text-gray-900 hover:opacity-80 transition-opacity">
                    <div className="bg-[#0F62FE] p-1.5 rounded-md shadow-sm">
                        <Rocket className="h-4 w-4 text-white" />
                    </div>
                    RepoPilot
                </Link>

                {/* Right Side Info */}
                <div className="flex items-center gap-4 text-sm text-gray-600">
                    <div className="hidden md:flex items-center gap-1.5 bg-gray-100 px-3 py-1.5 rounded-full text-xs font-medium text-gray-700">
                        <Zap className="h-3 w-3 text-[#0F62FE]" />
                        IBM Bob 2.0 Hackathon
                    </div>
                    <a
                        href="https://github.com/muragheshshirakol-tech/RepoPilot"
                        target="_blank"
                        rel="noopener noreferrer"
                        className="flex items-center gap-1.5 hover:text-[#0F62FE] transition-colors font-medium"
                    >
                        <Code className="h-4 w-4" /> {/* Swapped Github for Code */}
                        <span className="hidden sm:inline">Source</span>
                    </a>
                </div>
            </div>
        </nav>
    );
}