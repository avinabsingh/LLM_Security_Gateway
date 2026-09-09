import { useState } from "react";
import { Shield, Send, AlertOctagon, CheckCircle } from "lucide-react";
import RiskBadge from "../components/RiskBadge";
import RiskFactors from "../components/RiskFactors";

export default function Dashboard() {
  const [prompt, setPrompt] = useState("");
  const [report, setReport] = useState(null);
  const [isScanning, setIsScanning] = useState(false);
  const [error, setError] = useState(null);

  const analyzePrompt = async () => {
    if (!prompt.trim()) return;

    setIsScanning(true);
    setError(null);
    setReport(null);

    try {
      const response = await fetch("http://localhost:8000/api/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt: prompt }),
      });

      if (!response.ok)
        throw new Error("Failed to connect to the Security Gateway");

      const data = await response.json();

      // Successfully extracts the nested RiskReport object from AnalyzeResponse
      setReport(data.risk);
      console.log("Received RiskReport:", data);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsScanning(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-6 md:p-10 font-sans">
      <header className="flex items-center mb-8">
        <div className="bg-slate-900 p-3 rounded-xl mr-4">
          <Shield className="w-8 h-8 text-blue-400" />
        </div>
        <div>
          <h1 className="text-3xl font-extrabold text-slate-900">
            LLM Security Firewall
          </h1>
          <p className="text-slate-500 font-medium mt-1">
            Real-time Prompt Injection & Jailbreak Detection
          </p>
        </div>
      </header>

      <div className="bg-white rounded-2xl shadow-sm border border-slate-200 p-6 mb-8">
        <textarea
          className="w-full p-4 border-2 border-slate-200 rounded-xl mb-4 text-lg focus:outline-none focus:border-blue-500 transition-colors resize-y min-h-[120px]"
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="Enter a prompt to scan for malicious intent..."
        />

        <button
          onClick={analyzePrompt}
          disabled={isScanning || !prompt.trim()}
          className="w-full flex justify-center items-center bg-blue-600 text-white font-bold py-3.5 rounded-xl hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
        >
          {isScanning ? (
            <span className="flex items-center animate-pulse">
              <Shield className="w-5 h-5 mr-2" /> Scanning Payload...
            </span>
          ) : (
            <span className="flex items-center">
              <Send className="w-5 h-5 mr-2" /> Analyze Threat
            </span>
          )}
        </button>

        {error && (
          <div className="mt-4 p-4 bg-red-50 text-red-700 rounded-xl border border-red-200 text-sm font-medium">
            Error: {error}
          </div>
        )}
      </div>

      {report && (
        <div className="animate-in fade-in slide-in-from-bottom-4 duration-500">
          <div
            className={`p-6 rounded-2xl border-2 mb-6 flex flex-col md:flex-row items-start md:items-center justify-between ${
              report.decision === "BLOCK"
                ? "bg-red-50 border-red-200"
                : "bg-green-50 border-green-200"
            }`}
          >
            <div className="flex items-center mb-4 md:mb-0">
              {report.decision === "BLOCK" ? (
                <AlertOctagon className="w-10 h-10 text-red-600 mr-4" />
              ) : (
                <CheckCircle className="w-10 h-10 text-green-600 mr-4" />
              )}
              <div>
                <h2
                  className={`text-2xl font-black tracking-tight ${
                    report.decision === "BLOCK"
                      ? "text-red-900"
                      : "text-green-900"
                  }`}
                >
                  VERDICT: {report.decision}
                </h2>
                <p
                  className={`text-sm font-semibold mt-1 uppercase tracking-wider ${
                    report.decision === "BLOCK"
                      ? "text-red-700"
                      : "text-green-700"
                  }`}
                >
                  Reason:{" "}
                  {report?.decision_reason
                    ? report.decision_reason.replace(/_/g, " ")
                    : "N/A"}
                </p>
              </div>
            </div>

            <div className="flex flex-col items-end w-full md:w-auto bg-white p-3 rounded-xl shadow-sm border border-slate-100">
              <span className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-1">
                Risk Profile
              </span>
              <div className="flex items-center gap-3">
                <span className="font-mono text-xl font-bold text-slate-700">
                  {report.risk_score}%
                </span>
                <RiskBadge level={report.risk_level} />
              </div>
            </div>
          </div>

          <RiskFactors factors={report.top_risk_factors || []} />
        </div>
      )}
    </div>
  );
}
