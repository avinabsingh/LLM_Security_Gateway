import { useState } from "react";
import {
  Shield,
  Send,
  AlertOctagon,
  CheckCircle,
  Brain,
  Terminal,
  MessageSquare,
} from "lucide-react";
import RiskBadge from "../components/RiskBadge";
import RiskFactors from "../components/RiskFactors";
import { featureDictionary } from "../config/xaiConfig";

export default function Dashboard() {
  const [scanMode, setScanMode] = useState("direct"); // "direct" or "multi"
  const [prompt, setPrompt] = useState("");
  const [report, setReport] = useState(null);
  const [isScanning, setIsScanning] = useState(false);
  const [error, setError] = useState(null);

  // Track multi-turn state dynamically in the UI
  const [sessionId] = useState(
    () => "session_" + Math.random().toString(36).substring(2, 9),
  );
  const [turnHistory, setTurnHistory] = useState([]);

  const analyzePayload = async () => {
    if (!prompt.trim()) return;
    setIsScanning(true);
    setError(null);
    setReport(null);

    // Route dynamically based on mode
    const endpoint =
      scanMode === "multi"
        ? "http://localhost:8000/api/analyze/multi-turn"
        : "http://localhost:8000/api/analyze";

    const payload =
      scanMode === "multi"
        ? { prompt: prompt, session_id: sessionId }
        : { prompt: prompt };

    try {
      const response = await fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (!response.ok)
        throw new Error("Failed to connect to the Security Gateway");

      const data = await response.json();
      setReport(data.risk);

      // Add to UI history if in multi-turn mode
      if (scanMode === "multi") {
        setTurnHistory((prev) => {
          const newHistory = [
            ...prev,
            { text: prompt, risk: data.risk.risk_score },
          ];
          return newHistory.slice(-3); // Keep only last 3 turns
        });
        setPrompt(""); // Clear input for the next turn
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setIsScanning(false);
    }
  };

  const renderXAIAssessment = () => {
    if (
      !report ||
      report.decision !== "BLOCK" ||
      !report.top_risk_factors?.length
    )
      return null;

    const primaryFactor = report.top_risk_factors[0].feature;
    const meta = featureDictionary[primaryFactor];
    const primaryLabel = meta ? meta.label : primaryFactor;

    return (
      <div className="mt-4 p-4 bg-slate-50 border border-slate-200 rounded-lg text-sm text-slate-700 flex items-start space-x-3">
        <Brain className="w-5 h-5 text-blue-600 flex-shrink-0 mt-0.5" />
        <div>
          <span className="font-bold text-slate-900 mr-2">AI Assessment:</span>
          {scanMode === "multi" && primaryFactor === "Context_Drift" ? (
            <>
              Neutralized due to a{" "}
              <span className="font-bold text-red-700">
                Multi-Turn  Attack
              </span>
              . The session's risk velocity escalated across 3 turns, triggering
              our stateful context-drift guardrail.
            </>
          ) : (
            <>
              Neutralized primarily because it triggered our{" "}
              <span className="font-bold">{primaryLabel}</span> guardrail.
            </>
          )}
        </div>
      </div>
    );
  };

  return (
    <div className="max-w-4xl mx-auto p-6 md:p-10 font-sans">
      <header className="flex items-center justify-between mb-8">
        <div className="flex items-center">
          <div className="bg-slate-900 p-3 rounded-xl mr-4">
            <Shield className="w-8 h-8 text-blue-400" />
          </div>
          <div>
            <h1 className="text-3xl font-extrabold text-slate-900">
              LLM Security Firewall
            </h1>
            <p className="text-slate-500 font-medium mt-1">
              Real-time Prompt Injection Detection
            </p>
          </div>
        </div>
      </header>

      {/* Mode Switcher */}
      <div className="flex p-1 bg-slate-100 rounded-xl mb-6 max-w-md">
        <button
          onClick={() => {
            setScanMode("direct");
            setReport(null);
            setError(null);
          }}
          className={`flex-1 flex items-center justify-center py-2.5 px-4 rounded-lg text-sm font-bold transition-all ${
            scanMode === "direct"
              ? "bg-white text-slate-900 shadow-sm"
              : "text-slate-600 hover:text-slate-900"
          }`}
        >
          <Terminal className="w-4 h-4 mr-2" /> Single Prompt
        </button>
        <button
          onClick={() => {
            setScanMode("multi");
            setReport(null);
            setError(null);
            setTurnHistory([]);
          }}
          className={`flex-1 flex items-center justify-center py-2.5 px-4 rounded-lg text-sm font-bold transition-all ${
            scanMode === "multi"
              ? "bg-blue-600 text-white shadow-sm"
              : "text-slate-600 hover:text-slate-900"
          }`}
        >
          <MessageSquare className="w-4 h-4 mr-2" /> Multi-Turn 
        </button>
      </div>

      <div className="bg-white rounded-2xl shadow-sm border border-slate-200 p-6 mb-8">
        {/* Dynamic Multi-Turn Timeline */}
        {scanMode === "multi" && turnHistory.length > 0 && (
          <div className="mb-4 space-y-3 p-4 bg-slate-50 rounded-xl border border-slate-100">
            {turnHistory.map((turn, index) => (
              <div
                key={index}
                className="flex justify-between items-start text-sm pb-2 border-b border-slate-200 last:border-0 last:pb-0"
              >
                <div className="text-slate-600 pr-4">
                  <span className="font-bold text-slate-900">
                    Turn {index + 1}:
                  </span>{" "}
                  "{turn.text}"
                </div>
                <span
                  className={`text-xs font-bold px-2 py-1 rounded whitespace-nowrap ${
                    turn.risk > 50
                      ? "text-red-700 bg-red-100"
                      : turn.risk > 20
                        ? "text-yellow-700 bg-yellow-100"
                        : "text-green-700 bg-green-100"
                  }`}
                >
                  Risk: {turn.risk.toFixed(1)}%
                </span>
              </div>
            ))}
          </div>
        )}

        <textarea
          className="w-full p-4 border-2 border-slate-200 rounded-xl mb-4 text-base focus:outline-none focus:border-blue-500 transition-colors resize-y min-h-[140px]"
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder={
            scanMode === "multi"
              ? `Enter prompt for Turn ${turnHistory.length + 1}...`
              : "Enter user prompt to scan for malicious intent..."
          }
        />

        <button
          onClick={analyzePayload}
          disabled={isScanning || !prompt.trim()}
          className="w-full flex justify-center items-center text-white font-bold py-3.5 rounded-xl disabled:opacity-50 transition-all bg-blue-600 hover:bg-blue-700"
        >
          {isScanning ? "Scanning Payload..." : "Analyze Threat"}
        </button>
      </div>

      {/* Render Report UI (Same as before) */}
      {report && (
        <div className="animate-in fade-in slide-in-from-bottom-4 duration-500">
          <div
            className={`p-6 rounded-2xl border-2 mb-6 flex flex-col md:flex-row items-center justify-between ${report.decision === "BLOCK" ? "bg-red-50 border-red-200" : "bg-green-50 border-green-200"}`}
          >
            <div className="flex flex-col mb-4 md:mb-0 w-full md:w-auto">
              <div className="flex items-center">
                {report.decision === "BLOCK" ? (
                  <AlertOctagon className="w-10 h-10 text-red-600 mr-4" />
                ) : (
                  <CheckCircle className="w-10 h-10 text-green-600 mr-4" />
                )}
                <div>
                  <h2
                    className={`text-2xl font-black tracking-tight ${report.decision === "BLOCK" ? "text-red-900" : "text-green-900"}`}
                  >
                    VERDICT: {report.decision}
                  </h2>
                  <p
                    className={`text-sm font-semibold mt-1 uppercase tracking-wider ${report.decision === "BLOCK" ? "text-red-700" : "text-green-700"}`}
                  >
                    Reason:{" "}
                    {report?.decision_reason
                      ? report.decision_reason.replace(/_/g, " ")
                      : "N/A"}
                  </p>
                </div>
              </div>
              {renderXAIAssessment()}
            </div>
            <div className="flex flex-col items-end w-full md:w-auto bg-white p-3 rounded-xl shadow-sm border border-slate-100">
              <span className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-1">
                Risk Profile
              </span>
              <div className="flex items-center gap-3">
                <span className="font-mono text-xl font-bold text-slate-700">
                  {report.risk_score}%
                </span>
                <RiskBadge
                  level={report.risk_level}
                  score={report.risk_score}
                />
              </div>
            </div>
          </div>
          <RiskFactors factors={report.top_risk_factors || []} />
        </div>
      )}
    </div>
  );
}
