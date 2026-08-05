import Badge from "./Badge";
import Card from "./Card";
import ProgressBar from "./ProgressBar";
import Skeleton from "./Skeleton";

function SignalPanel({ result, loading }) {
  if (loading) return <Card className="p-5" hover={false}><Skeleton className="h-4 w-24" /><Skeleton className="mt-5 h-11 w-36" /><div className="mt-6 grid grid-cols-2 gap-3"><Skeleton className="h-20" /><Skeleton className="h-20" /></div><Skeleton className="mt-5 h-3 w-full" /></Card>;

  const action = result?.action || "WAITING";
  const variant = action.includes("BUY") ? "success" : action.includes("SELL") ? "danger" : "warning";
  const tone = action.includes("BUY") ? "green" : action.includes("SELL") ? "red" : "amber";
  const confidence = result?.confidence ?? 0;
  const strength = action.includes("STRONG") ? "STRONG" : result ? "NORMAL" : "—";
  const risk = result?.risk || "—";
  const riskTone = risk === "HIGH" ? "danger" : risk === "MEDIUM" ? "warning" : risk === "LOW" ? "success" : "neutral";

  const heights = ["h-3", "h-4", "h-5", "h-6", "h-7"];
  const meterColor = tone === "green" ? "bg-[#22C55E]" : tone === "red" ? "bg-[#EF4444]" : "bg-amber-400";

  return <Card className="p-5"><p className="text-xs font-semibold uppercase tracking-[0.16em] text-[#9CA3AF]">Signal intelligence</p><div className="mt-4 flex items-center justify-between gap-3"><div className={`rounded-xl border px-4 py-2 text-lg font-black tracking-wide shadow-[0_0_24px_rgba(59,130,246,0.14)] transition duration-200 ${variant === "success" ? "border-[#22C55E]/40 bg-[#22C55E]/10 text-[#86EFAC]" : variant === "danger" ? "border-[#EF4444]/40 bg-[#EF4444]/10 text-[#FCA5A5]" : "border-amber-400/40 bg-amber-400/10 text-amber-200"}`}>{action}</div><Badge variant={riskTone}>RISK {risk}</Badge></div><div className="mt-6"><div className="flex justify-between text-xs"><span className="text-[#9CA3AF]">Confidence</span><span className="font-semibold text-[#E5E7EB]">{result ? `${confidence}%` : "—"}</span></div><ProgressBar value={confidence} tone={tone} className="mt-2" /></div><div className="mt-5 flex items-end justify-between"><div><p className="text-xs text-[#9CA3AF]">Signal strength</p><p className="mt-1 text-sm font-semibold text-[#E5E7EB]">{strength}</p></div><div className="flex gap-1">{heights.map((height, index) => <span key={height} className={`${height} w-1 rounded-full ${result && (strength === "STRONG" ? true : index < 3) ? meterColor : "bg-[#374151]"}`} />)}</div></div></Card>;
}

export default SignalPanel;
