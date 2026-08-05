import { useEffect, useState } from "react";
import Card from "./Card";
import Skeleton from "./Skeleton";

function AIInsights({ insights, loading, onRegenerate }) {
  const [visibleCount, setVisibleCount] = useState(0);

  useEffect(() => {
    setVisibleCount(0);
    if (loading) return undefined;
    let count = 0;
    const timer = window.setInterval(() => {
      count += 1;
      setVisibleCount(count);
      if (count >= insights.length) window.clearInterval(timer);
    }, 180);
    return () => window.clearInterval(timer);
  }, [insights, loading]);

  return <Card className="p-5"><div className="flex items-center justify-between gap-3"><div className="flex items-center gap-3"><span className="grid h-8 w-8 place-items-center rounded-lg border border-[#3B82F6]/30 bg-[#3B82F6]/10 text-sm text-blue-200">✦</span><div><h2 className="text-sm font-semibold text-[#E5E7EB]">AI Copilot</h2><p className="text-xs text-[#9CA3AF]">Live signal rationale</p></div></div><span className="h-2 w-2 animate-pulse rounded-full bg-[#22C55E]" /></div>{loading ? <div className="mt-5 space-y-3"><Skeleton className="h-4 w-full" /><Skeleton className="h-4 w-5/6" /><Skeleton className="h-4 w-4/6" /></div> : <ul className="mt-5 space-y-3">{insights.slice(0, visibleCount).map((insight, index) => <li key={`${insight}-${index}`} className="soft-fade-in flex gap-3 text-sm leading-6 text-[#9CA3AF]"><span className="mt-2 grid h-3.5 w-3.5 shrink-0 place-items-center rounded-full bg-[#3B82F6]/15 text-[8px] text-blue-200">✦</span>{insight}</li>)}</ul>}<button onClick={onRegenerate} disabled={loading} className="mt-6 w-full rounded-lg border border-[#374151] bg-[#0B0F14] px-3 py-2 text-sm font-medium text-[#E5E7EB] transition duration-200 hover:border-[#3B82F6] hover:bg-[#3B82F6]/10 active:scale-95 disabled:opacity-50">Regenerate analysis</button></Card>;
}

export default AIInsights;
