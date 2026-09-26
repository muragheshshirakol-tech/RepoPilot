"use client";

import { useState, useRef, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { Loader2, Send, MessageSquare, FileCode } from "lucide-react";

interface Citation {
    path: string;
    start: number;
    end: number;
}

interface Message {
    id: string;
    role: "user" | "ai";
    content: string;
    citations?: Citation[];
}

interface QAPanelProps {
    jobId: string;
    onCitationClick?: (citation: Citation) => void;
}

export function QAPanel({ jobId, onCitationClick }: QAPanelProps) {
    const [messages, setMessages] = useState<Message[]>([
        {
            id: "welcome",
            role: "ai",
            content: "Hi! I've analyzed this repository. Ask me anything about its architecture, business logic, or how specific features work.",
        },
    ]);
    const [input, setInput] = useState("");
    const [isLoading, setIsLoading] = useState(false);
    const messagesEndRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [messages]);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!input.trim() || isLoading) return;

        const userMessage: Message = { id: Date.now().toString(), role: "user", content: input };
        setMessages((prev) => [...prev, userMessage]);
        setInput("");
        setIsLoading(true);

        try {
            const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
            const res = await fetch(`${apiUrl}/api/repos/${jobId}/ask`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ question: userMessage.content }),
            });

            if (!res.ok) throw new Error("Failed to get answer.");

            const data = await res.json();

            const aiMessage: Message = {
                id: (Date.now() + 1).toString(),
                role: "ai",
                content: data.answer || "I couldn't find enough information to answer that.",
                citations: data.citations || [],
            };
            setMessages((prev) => [...prev, aiMessage]);
        } catch (err) {
            const errorMessage: Message = {
                id: (Date.now() + 1).toString(),
                role: "ai",
                content: "Sorry, I encountered an error connecting to the brain. Please try again.",
            };
            setMessages((prev) => [...prev, errorMessage]);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <Card className="h-full flex flex-col border-t-4 border-t-green-500">
            <CardHeader className="pb-3 border-b">
                <CardTitle className="text-lg font-bold flex items-center gap-2">
                    <MessageSquare className="h-5 w-5 text-green-500" />
                    Grounded Q&A
                </CardTitle>
            </CardHeader>

            {/* Messages Area */}
            <CardContent className="flex-1 overflow-y-auto p-4 space-y-4 bg-gray-50/50">
                {messages.map((msg) => (
                    <div key={msg.id} className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}>
                        <div className={`max-w-[85%] rounded-lg p-3 ${msg.role === "user" ? "bg-[#0F62FE] text-white" : "bg-white border text-gray-800 shadow-sm"
                            }`}>
                            <p className="text-sm whitespace-pre-wrap leading-relaxed">{msg.content}</p>

                            {/* Citations */}
                            {msg.role === "ai" && msg.citations && msg.citations.length > 0 && (
                                <div className="mt-3 flex flex-wrap gap-2 border-t pt-2 border-gray-200">
                                    <span className="text-[10px] font-bold text-gray-400 uppercase tracking-wider w-full">Sources:</span>
                                    {msg.citations.map((cite, idx) => (
                                        <button
                                            key={idx}
                                            onClick={() => onCitationClick?.(cite)}
                                            className="flex items-center gap-1 bg-gray-100 hover:bg-gray-200 text-gray-700 px-2 py-1 rounded text-[10px] font-mono transition-colors"
                                            title={`Go to ${cite.path}:${cite.start}`}
                                        >
                                            <FileCode className="h-3 w-3" />
                                            {cite.path.split("/").pop()}:{cite.start}
                                        </button>
                                    ))}
                                </div>
                            )}
                        </div>
                    </div>
                ))}

                {isLoading && (
                    <div className="flex justify-start">
                        <div className="bg-white border rounded-lg p-3 shadow-sm flex items-center gap-2 text-gray-500">
                            <Loader2 className="h-4 w-4 animate-spin text-[#0F62FE]" />
                            <span className="text-sm">Thinking...</span>
                        </div>
                    </div>
                )}
                <div ref={messagesEndRef} />
            </CardContent>

            {/* Input Area */}
            <div className="p-4 border-t bg-white">
                <form onSubmit={handleSubmit} className="flex gap-2">
                    <Input
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        placeholder="Ask about the codebase..."
                        disabled={isLoading}
                        className="flex-1"
                    />
                    <Button
                        type="submit"
                        disabled={isLoading || !input.trim()}
                        className="bg-[#0F62FE] hover:bg-[#0353E9] text-white"
                    >
                        {isLoading ? <Loader2 className="h-4 w-4 animate-spin" /> : <Send className="h-4 w-4" />}
                    </Button>
                </form>
            </div>
        </Card>
    );
}