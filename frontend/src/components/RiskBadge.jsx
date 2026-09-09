import { ShieldCheck, AlertTriangle, ShieldAlert, Skull } from 'lucide-react';

export default function RiskBadge({ level }) {
  const config = {
    LOW: {
      color: 'bg-green-100 text-green-700 border-green-300',
      icon: <ShieldCheck className="w-5 h-5 mr-1.5" />
    },
    MEDIUM: {
      color: 'bg-yellow-100 text-yellow-700 border-yellow-300',
      icon: <AlertTriangle className="w-5 h-5 mr-1.5" />
    },
    HIGH: {
      color: 'bg-orange-100 text-orange-700 border-orange-300',
      icon: <ShieldAlert className="w-5 h-5 mr-1.5" />
    },
    CRITICAL: {
      color: 'bg-red-100 text-red-700 border-red-300',
      icon: <Skull className="w-5 h-5 mr-1.5" />
    }
  };

  const current = config[level] || config.LOW;

  return (
    <div className={`flex items-center px-3 py-1.5 rounded-full border font-bold text-sm ${current.color}`}>
      {current.icon}
      {level || "UNKNOWN"}
    </div>
  );
}