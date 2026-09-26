"use client";

import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { oneDark } from "react-syntax-highlighter/dist/esm/styles/prism";
import { ChevronLeft, ChevronRight, FileCode, BookOpen } from "lucide-react";

interface TourStep {
    step: number;
    title: string;
    path: string;
    start: number;
    end: number;
    narration: string;
    code?: string;
}

interface CodeTourViewerProps {
    steps: TourStep[];
    activeStepIndex?: number; // NEW: Allow external control
}

export function CodeTourViewer({ steps, activeStepIndex }: CodeTourViewerProps) {
    const [internalStepIndex, setInternalStepIndex] = useState(0);

    // Use external prop if provided, otherwise use internal state
    const currentStepIndex = activeStepIndex !== undefined ? activeStepIndex : internalStepIndex;

    useEffect(() => {
        const handleKeyDown = (e: KeyboardEvent) => {
            if (e.key.toLowerCase() === "j") handleNext();
            if (e.key.toLowerCase() === "k") handlePrev();
        };
        window.addEventListener("keydown", handleKeyDown);
        return () => window.removeEventListener("keydown", handleKeyDown);
    }, [currentStepIndex]);

    const handleNext = () => {
        if (currentStepIndex < steps.length - 1) {
            if (activeStepIndex === undefined) setInternalStepIndex(currentStepIndex + 1);
        }
    };

    const handlePrev = () => {
        if (currentStepIndex > 0) {
            if (activeStepIndex === undefined) setInternalStepIndex(currentStepIndex - 1);
        }
    };

    if (!steps || steps.length === 0) {
        return (
            <Card className="h-full flex items-center justify-center">
                <CardContent className="text-center text-gray-500">
                    <BookOpen className="mx-auto h-12 w-12 mb-4 opacity-50" />
                    <p>No code tour steps generated yet.</p>
                </CardContent>
            </Card>
        );
    }

    const step = steps[currentStepIndex];

    return (
        <Card className="h-full flex flex-col border-t-4 border-t-[#0F62FE]">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-4 border-b">
                <div className="flex items-center gap-3">
                    <FileCode className="h-6 w-6 text-[#0F62FE]" />
                    <div>
                        <CardTitle className="text-lg font-bold">{step.title}</CardTitle>
                        <p className="text-xs text-gray-500 font-mono mt-1">
                            {step.path} (Lines {step.start}-{step.end})
                        </p>
                    </div>
                </div>
                <Badge variant="outline" className="bg-gray-100">
                    Step {currentStepIndex + 1} of {steps.length}
                </Badge>
            </CardHeader>

            <CardContent className="flex-1 flex flex-col p-0">
                <div className="p-4 bg-blue-50/50 border-b">
                    <p className="text-sm text-gray-800 leading-relaxed italic">
                        "{step.narration}"
                    </p>
                </div>

                <div className="flex-1 overflow-auto bg-[#282c34]">
                    <SyntaxHighlighter
                        language={step.path.endsWith(".py") ? "python" : step.path.endsWith(".ts") || step.path.endsWith(".tsx") ? "typescript" : "javascript"}
                        style={oneDark}
                        showLineNumbers={true}
                        startingLineNumber={step.start}
                        wrapLines={true}
                        customStyle={{ margin: 0, padding: "1rem", background: "transparent", fontSize: "0.85rem" }}
                    >
                        {step.code || `// Code snippet for ${step.path}\n// Lines ${step.start} to ${step.end}\n// (Backend will inject actual code here)`}
                    </SyntaxHighlighter>
                </div>

                <div className="p-4 border-t flex justify-between items-center bg-gray-50">
                    <Button
                        variant="outline"
                        onClick={handlePrev}
                        disabled={currentStepIndex === 0}
                        className="flex items-center gap-2"
                    >
                        <ChevronLeft className="h-4 w-4" /> Previous
                    </Button>
                    <p className="text-xs text-gray-500">Press <kbd className="px-1 py-0.5 bg-gray-200 rounded">j</kbd> / <kbd className="px-1 py-0.5 bg-gray-200 rounded">k</kbd> to navigate</p>
                    <Button
                        variant="default"
                        onClick={handleNext}
                        disabled={currentStepIndex === steps.length - 1}
                        className="flex items-center gap-2 bg-[#0F62FE] hover:bg-[#0353E9]"
                    >
                        Next <ChevronRight className="h-4 w-4" />
                    </Button>
                </div>
            </CardContent>
        </Card>
    );
}