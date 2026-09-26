"use client";

import { useRouter } from "next/navigation";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { Button } from "@/components/ui/button";
import { Loader2, CheckCircle2, AlertCircle, Brain, Cpu, ArrowRight } from "lucide-react";
import { useWebSocket, AgentEvent } from "@/lib/useWebSocket";

export default function AnalysisPage({ params }: { params: { jobId: string } }) {
    const router = useRouter();

    // Renamed to wsStatus to avoid shadowing conflicts with component props
    const { status: wsStatus, events, error } = useWebSocket(params.jobId);

    // Determine overall pipeline progress based on completed nodes
    const completedNodes = new Set(
        events
            .filter((e: AgentEvent) => e.event === "agent_progress" && e.status === "done")
            .map((e: AgentEvent) => e.node)
    );

    const totalNodes = 5; // ingest, parse, fanout, synthesize, emit
    const progress = Math.min(100, Math.round((completedNodes.size / totalNodes) * 100));
    const isComplete = events.some((e: AgentEvent) => e.event === "complete");

    // Helper to get the latest status of a specific node
    const getNodeStatus = (nodeName: string) => {
        const nodeEvents = events.filter((e: AgentEvent) => e.node === nodeName);
        if (nodeEvents.length === 0) return "pending";
        return nodeEvents[nodeEvents.length - 1].status || "pending";
    };

    // Renamed prop to 'nodeStatus' to prevent variable shadowing with 'wsStatus'
    const StatusBadge = ({ nodeStatus }: { nodeStatus: string }) => {
        if (nodeStatus === "done") return <Badge className="bg-green-500 hover:bg-green-600"><CheckCircle2 className="w-3 h-3 mr-1" /> Done</Badge>;
        if (nodeStatus === "running" || nodeStatus === "processing") return <Badge className="bg-blue-500 hover:bg-blue-600"><Loader2 className="w-3 h-3 mr-1 animate-spin" /> Running</Badge>;
        if (nodeStatus === "failed") return <Badge variant="destructive"><AlertCircle className="w-3 h-3 mr-1" /> Failed</Badge>;
        return <Badge variant="outline" className="text-gray-500">Pending</Badge>;
    };

    return (
        <main className="min-h-screen bg-gray-50 p-6 md:p-12">
            <div className="max-w-4xl mx-auto space-y-8">

                {/* Header & Progress */}
                <div className="space-y-4">
                    <div className="flex items-center justify-between">
                        <div>
                            <h1 className="text-3xl font-bold text-gray-900">Live Analysis</h1>
                            <p className="text-gray-500 mt-1">Job ID: <span className="font-mono text-sm bg-gray-200 px-2 py-1 rounded">{params.jobId}</span></p>
                        </div>
                        <div className="text-right">
                            <p className="text-sm font-medium text-gray-700">Overall Progress</p>
                            <p className="text-2xl font-bold text-[#0F62FE]">{progress}%</p>
                        </div>
                    </div>
                    <Progress value={progress} className="h-3" />
                </div>

                {/* Error State */}
                {error && (
                    <Card className="border-red-200 bg-red-50">
                        <CardContent className="flex items-center gap-3 p-4 text-red-700">
                            <AlertCircle className="h-5 w-5" />
                            <p>{error}</p>
                        </CardContent>
                    </Card>
                )}

                {/* Agent Cards Grid */}
                <div className="grid md:grid-cols-2 gap-6">
                    {/* Architecture Agent Card */}
                    <Card className={`border-t-4 border-t-[#0F62FE] transition-all ${getNodeStatus("fanout") === "running" ? "ring-2 ring-[#0F62FE]/20" : ""}`}>
                        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                            <CardTitle className="text-lg font-bold flex items-center gap-2">
                                <Brain className="h-5 w-5 text-[#0F62FE]" />
                                Architecture Agent
                            </CardTitle>
                            <StatusBadge nodeStatus={getNodeStatus("fanout")} />
                        </CardHeader>
                        <CardContent>
                            <p className="text-sm text-gray-600 mb-4">
                                Mapping top modules, entry points, and dominant data flow.
                            </p>
                            <div className="space-y-2">
                                <div className="flex justify-between text-xs text-gray-500">
                                    <span>Context Ingestion</span>
                                    <span>{getNodeStatus("ingest") === "done" ? "✓" : "..."}</span>
                                </div>
                                <div className="flex justify-between text-xs text-gray-500">
                                    <span>AST Parsing</span>
                                    <span>{getNodeStatus("parse") === "done" ? "✓" : "..."}</span>
                                </div>
                            </div>
                        </CardContent>
                    </Card>

                    {/* Business Logic Agent Card */}
                    <Card className={`border-t-4 border-t-purple-500 transition-all ${getNodeStatus("fanout") === "running" ? "ring-2 ring-purple-500/20" : ""}`}>
                        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                            <CardTitle className="text-lg font-bold flex items-center gap-2">
                                <Cpu className="h-5 w-5 text-purple-500" />
                                Business Logic Agent
                            </CardTitle>
                            <StatusBadge nodeStatus={getNodeStatus("fanout")} />
                        </CardHeader>
                        <CardContent>
                            <p className="text-sm text-gray-600 mb-4">
                                Identifying core domain concepts, invariants, and state transitions.
                            </p>
                            <div className="space-y-2">
                                <div className="flex justify-between text-xs text-gray-500">
                                    <span>Context Ingestion</span>
                                    <span>{getNodeStatus("ingest") === "done" ? "✓" : "..."}</span>
                                </div>
                                <div className="flex justify-between text-xs text-gray-500">
                                    <span>AST Parsing</span>
                                    <span>{getNodeStatus("parse") === "done" ? "✓" : "..."}</span>
                                </div>
                            </div>
                        </CardContent>
                    </Card>
                </div>

                {/* Completion Action */}
                {isComplete && (
                    <div className="flex justify-center pt-4 animate-in fade-in slide-in-from-bottom-4">
                        <Button
                            onClick={() => router.push(`/onboarding/${params.jobId}`)}
                            className="bg-[#0F62FE] hover:bg-[#0353E9] text-white font-semibold px-8 py-6 text-lg shadow-lg"
                        >
                            View Onboarding Dashboard
                            <ArrowRight className="ml-2 h-5 w-5" />
                        </Button>
                    </div>
                )}

            </div>
        </main>
    );
}