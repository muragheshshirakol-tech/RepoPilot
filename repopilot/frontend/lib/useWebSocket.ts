"use client";

import { useEffect, useRef, useState } from "react";

export interface AgentEvent {
    event: string;
    node?: string;
    status?: string;
    findings_count?: number;
    error?: string;
    job_id?: string;
}

export function useWebSocket(jobId: string) {
    const [status, setStatus] = useState<"connecting" | "connected" | "closed" | "error">("connecting");
    const [events, setEvents] = useState<AgentEvent[]>([]);
    const [error, setError] = useState<string | null>(null);
    const wsRef = useRef<WebSocket | null>(null);

    useEffect(() => {
        if (!jobId) return;

        const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
        const wsProtocol = apiUrl.startsWith("https") ? "wss" : "ws";
        const wsUrl = `${wsProtocol}://${apiUrl.split("://")[1]}/api/repos/${jobId}/stream`;

        const socket = new WebSocket(wsUrl);
        wsRef.current = socket;

        socket.onopen = () => {
            setStatus("connected");
            setError(null);
        };

        socket.onmessage = (event) => {
            try {
                const data: AgentEvent = JSON.parse(event.data);
                setEvents((prev) => [...prev, data]);
            } catch (e) {
                console.error("WebSocket parse error:", e);
            }
        };

        socket.onclose = () => {
            setStatus("closed");
        };

        socket.onerror = () => {
            setStatus("error");
            setError("Cannot connect to analysis stream. Is the backend running?");
        };

        return () => {
            socket.close();
        };
    }, [jobId]);

    return { status, events, error };
}