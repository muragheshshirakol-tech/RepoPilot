export const mockOnboardingPlan = {
    role: "Frontend",
    architecture_summary: "This is a modern Next.js 14 application using the App Router. It follows a feature-sliced design pattern, with UI components isolated in the `/components` directory and business logic handled by Server Actions in `/actions`. State management is minimal, relying on React Server Components and URL search params for caching and sharing state.",
    key_concepts: [
        "Next.js App Router and Server Components",
        "Tailwind CSS and shadcn/ui for styling",
        "Server Actions for form mutations",
        "Middleware for authentication routing"
    ],
    tour_steps: [
        {
            step: 1,
            title: "Application Entry Point",
            path: "app/page.tsx",
            start: 1,
            end: 25,
            narration: "This is the main landing page. It fetches data on the server and passes it to the Client Component for interactive rendering.",
            code: `"use client";\n\nimport { Button } from "@/components/ui/button";\n\nexport default function Home() {\n  return (\n    <main className="flex min-h-screen flex-col items-center justify-between p-24">\n      <h1 className="text-4xl font-bold">Welcome to RepoPilot</h1>\n      <Button>Get Started</Button>\n    </main>\n  );\n}`
        },
        {
            step: 2,
            title: "Global Layout & Font Setup",
            path: "app/layout.tsx",
            start: 1,
            end: 30,
            narration: "The root layout defines the HTML shell, injects the IBM Plex Sans font, and wraps the application in necessary providers.",
            code: `import type { Metadata } from "next";\nimport { Inter } from "next/font/google";\nimport "./globals.css";\n\nconst inter = Inter({ subsets: ["latin"] });\n\nexport const metadata: Metadata = {\n  title: "RepoPilot",\n  description: "AI-powered developer onboarding",\n};\n\nexport default function RootLayout({ children }: { children: React.ReactNode }) {\n  return (\n    <html lang="en">\n      <body className={inter.className}>{children}</body>\n    </html>\n  );\n}`
        },
        {
            step: 3,
            title: "API Route Handler",
            path: "app/api/repos/route.ts",
            start: 1,
            end: 20,
            narration: "This POST endpoint handles incoming repository submission requests, validates the payload, and triggers the background analysis job.",
            code: `import { NextResponse } from "next/server";\nimport { v4 as uuidv4 } from "uuid";\n\nexport async function POST(req: Request) {\n  try {\n    const body = await req.json();\n    const { repo_url, role } = body;\n    \n    if (!repo_url || !role) {\n      return NextResponse.json({ error: "Missing fields" }, { status: 400 });\n    }\n\n    const job_id = uuidv4();\n    // Trigger background job here\n    \n    return NextResponse.json({ job_id, status: "queued" });\n  } catch (error) {\n    return NextResponse.json({ error: "Invalid request" }, { status: 400 });\n  }\n}`
        }
    ]
};