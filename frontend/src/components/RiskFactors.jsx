import { Activity } from "lucide-react";

export default function RiskFactors({ factors }) {
  if (!factors || factors.length === 0) return null;

  return (
    <div className="mt-6 border border-slate-200 rounded-xl overflow-hidden bg-white shadow-sm">
      <div className="bg-slate-50 px-5 py-4 border-b border-slate-200">
        <h3 className="font-semibold text-slate-800 flex items-center">
          <Activity className="w-4 h-4 mr-2 text-blue-600" />
          Top Risk Factors (Model Weights)
        </h3>
      </div>

      <ul className="divide-y divide-slate-100">
        {factors.map((factor, index) => (
          <li
            key={index}
            className="px-5 py-3 flex justify-between items-center hover:bg-slate-50 transition-colors"
          >
            <span className="font-mono text-sm text-slate-700 font-medium">
              {factor.feature}
            </span>
            <span
              className={`font-mono text-sm px-2.5 py-1 rounded-md ${
                factor.contribution > 0
                  ? "bg-rose-100 text-rose-700"
                  : "bg-emerald-100 text-emerald-700"
              }`}
            >
              {factor.contribution > 0 ? "+" : ""}
              {factor.contribution.toFixed(4)}
            </span>
          </li>
        ))}
      </ul>
    </div>
  );
}
