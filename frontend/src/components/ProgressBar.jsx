function ProgressBar({ value = 0, tone = "blue", className = "" }) {
  const colors = { blue: "bg-[#3B82F6]", green: "bg-[#22C55E]", red: "bg-[#EF4444]", amber: "bg-amber-400" };
  const safeValue = Math.max(0, Math.min(100, Number(value) || 0));

  return <div className={`h-2 overflow-hidden rounded-full bg-[#0B0F14] ${className}`}><div className={`h-full rounded-full transition-all duration-500 ease-in-out ${colors[tone]}`} style={{ width: `${safeValue}%` }} /></div>;
}

export default ProgressBar;
