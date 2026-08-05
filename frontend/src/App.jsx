import { useState } from "react";
import AIInsights from "./components/AIInsights";
import Card from "./components/Card";
import SignalPanel from "./components/SignalPanel";
import Skeleton from "./components/Skeleton";
import TradingChart from "./components/TradingChart";
import Watchlist from "./components/Watchlist";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://127.0.0.1:8000";
const navigation = ["Dashboard", "Markets", "Watchlist", "Alerts", "Settings"];
const searchResults = ["AAPL", "NVDA", "MSFT", "TSLA", "AMZN"];

function Icon({ name, className = "" }) {
  const paths = {
    Dashboard: <><rect x="3" y="3" width="7" height="7" rx="1" /><rect x="14" y="3" width="7" height="7" rx="1" /><rect x="3" y="14" width="7" height="7" rx="1" /><rect x="14" y="14" width="7" height="7" rx="1" /></>,
    Markets: <><path d="M3 17 9 11l4 4 7-8" /><path d="M15 7h5v5" /></>,
    Watchlist: <><path d="m12 3 2.8 5.7 6.2.9-4.5 4.4 1.1 6.2-5.6-3-5.6 3 1.1-6.2L3 9.6l6.2-.9z" /></>,
    Alerts: <><path d="M18 9a6 6 0 0 0-12 0c0 7-3 7-3 9h18c0-2-3-2-3-9" /><path d="M10 22h4" /></>,
    Settings: <><circle cx="12" cy="12" r="3" /><path d="M19.4 15a1.7 1.7 0 0 0 .34 1.88l.06.06-2.1 2.1-.06-.06a1.7 1.7 0 0 0-1.88-.34 1.7 1.7 0 0 0-1.04 1.56v.1h-3v-.1a1.7 1.7 0 0 0-1.04-1.56 1.7 1.7 0 0 0-1.88.34l-.06.06-2.1-2.1.06-.06A1.7 1.7 0 0 0 7.04 15 1.7 1.7 0 0 0 5.5 14H5.4v-3h.1A1.7 1.7 0 0 0 7.04 9.96a1.7 1.7 0 0 0-.34-1.88l-.06-.06 2.1-2.1.06.06a1.7 1.7 0 0 0 1.88.34A1.7 1.7 0 0 0 11.72 4.8v-.1h3v.1a1.7 1.7 0 0 0 1.04 1.52 1.7 1.7 0 0 0 1.88-.34l.06-.06 2.1 2.1-.06.06a1.7 1.7 0 0 0-.34 1.88A1.7 1.7 0 0 0 20.9 11h.1v3h-.1A1.7 1.7 0 0 0 19.4 15Z" /></>,
    Search: <><circle cx="11" cy="11" r="6" /><path d="m20 20-4-4" /></>,
    Bell: <><path d="M18 9a6 6 0 0 0-12 0c0 7-3 7-3 9h18c0-2-3-2-3-9" /><path d="M10 22h4" /></>,
    Menu: <><path d="M4 6h16" /><path d="M4 12h16" /><path d="M4 18h16" /></>,
    Chevron: <path d="m9 18 6-6-6-6" />,
  };
  return <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">{paths[name]}</svg>;
}

function App() {
  const [symbol, setSymbol] = useState("AAPL");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [timeframe, setTimeframe] = useState("1D");
  const [activeNav, setActiveNav] = useState("Dashboard");
  const [searchFocused, setSearchFocused] = useState(false);
  const [toast, setToast] = useState("");

  const requestAnalysis = async (requestedSymbol = symbol) => {
    const cleanSymbol = requestedSymbol.trim().toUpperCase();
    if (!cleanSymbol) return;
    setSymbol(cleanSymbol);
    setLoading(true);
    setResult(null);

    try {
      const response = await fetch(`${API_BASE_URL}/analyze/${encodeURIComponent(cleanSymbol)}`);
      if (!response.ok) {
        const error = await response.json().catch(() => null);
        throw new Error(error?.detail || `API request failed (${response.status})`);
      }
      setResult(await response.json());
      setToast(`${cleanSymbol} analysis is ready`);
      window.setTimeout(() => setToast(""), 3500);
    } catch (error) {
      setResult({ error: error instanceof TypeError ? "Cannot connect to the backend. Start it on http://127.0.0.1:8000 and try again." : error.message });
    } finally {
      setLoading(false);
      setSearchFocused(false);
    }
  };

  const insights = result ? [
    result.technical || "Technical indicators are awaiting data.",
    `${result.trend || "Current"} trend with ${result.risk?.toLowerCase() || "unknown"} risk.`,
    `News sentiment is ${result.sentiment?.toLowerCase() || "neutral"}.`,
    result.explanation || "No additional explanation is available.",
  ] : [
    "Search a symbol to generate a technical signal.",
    "Candles include a 20-day moving-average overlay.",
    "Buy and sell arrows are generated from RSI thresholds.",
  ];
  const filteredResults = searchResults.filter((item) => item.includes(symbol.trim().toUpperCase())).slice(0, 4);

  return <div className="min-h-screen bg-[#0B0F14] pb-20 font-sans text-[#E5E7EB] md:pb-0">
    <aside className={`fixed inset-y-0 left-0 z-30 hidden flex-col border-r border-[#1F2937] bg-[#0B0F14]/95 px-3 py-5 backdrop-blur-xl transition-[width] duration-200 ease-in-out md:flex ${sidebarOpen ? "w-64" : "w-[76px]"}`}>
      <div className="flex h-10 items-center justify-between px-2"><div className="flex items-center gap-3 overflow-hidden"><div className="grid h-9 w-9 shrink-0 place-items-center rounded-xl bg-gradient-to-br from-[#60A5FA] to-[#2563EB] text-sm font-black text-white shadow-lg shadow-blue-500/20">TM</div>{sidebarOpen && <span className="whitespace-nowrap text-base font-semibold tracking-tight">TradeMind <span className="text-[#60A5FA]">AI</span></span>}</div><button onClick={() => setSidebarOpen((open) => !open)} className="grid h-8 w-8 shrink-0 place-items-center rounded-lg text-[#9CA3AF] transition duration-200 hover:bg-[#1F2937] hover:text-white active:scale-95" aria-label="Toggle sidebar"><Icon name="Menu" className="h-5 w-5" /></button></div>
      <p className={`mt-10 px-3 text-[10px] font-semibold uppercase tracking-[0.2em] text-[#6B7280] ${sidebarOpen ? "" : "sr-only"}`}>Workspace</p>
      <nav className="mt-3 space-y-1">{navigation.map((item) => { const active = activeNav === item; return <button key={item} onClick={() => setActiveNav(item)} className={`group relative flex w-full items-center gap-3 rounded-xl px-3 py-3 text-sm transition duration-200 ${active ? "bg-[#3B82F6]/15 text-blue-200" : "text-[#9CA3AF] hover:bg-[#1F2937] hover:text-[#E5E7EB]"}`}><Icon name={item} className="h-5 w-5 shrink-0" />{sidebarOpen && <span>{item}</span>}{!sidebarOpen && <span className="pointer-events-none absolute left-14 z-50 hidden whitespace-nowrap rounded-md border border-[#374151] bg-[#111827] px-2 py-1 text-xs text-[#E5E7EB] shadow-xl group-hover:block">{item}</span>}</button>; })}</nav>
      <div className="mt-auto rounded-xl border border-[#1F2937] bg-[#111827]/90 p-3"><div className="flex items-center gap-2"><div className="grid h-8 w-8 shrink-0 place-items-center rounded-lg bg-[#3B82F6]/10 text-xs text-blue-200">⚡</div>{sidebarOpen && <div><p className="text-xs font-semibold text-[#E5E7EB]">Free plan</p><p className="text-[11px] text-[#9CA3AF]">5 analyses left</p></div>}</div>{sidebarOpen && <button className="mt-3 w-full rounded-lg bg-[#3B82F6] px-3 py-2 text-xs font-semibold text-white transition duration-200 hover:bg-blue-500 active:scale-95">Upgrade plan</button>}</div>
    </aside>

    <div className={`min-h-screen transition-[padding] duration-200 ease-in-out ${sidebarOpen ? "md:pl-64" : "md:pl-[76px]"}`}>
      <header className="sticky top-0 z-20 flex h-[72px] items-center gap-3 border-b border-[#1F2937] bg-[#0B0F14]/80 px-4 backdrop-blur-xl md:px-7"><button onClick={() => setSidebarOpen((open) => !open)} className="grid h-10 w-10 place-items-center rounded-xl border border-[#1F2937] text-[#9CA3AF] md:hidden" aria-label="Open navigation"><Icon name="Menu" className="h-5 w-5" /></button><form onSubmit={(event) => { event.preventDefault(); requestAnalysis(); }} className="relative flex min-w-0 flex-1 items-center gap-2 md:max-w-md"><div className="flex min-w-0 flex-1 items-center gap-2 rounded-xl border border-[#1F2937] bg-[#111827]/80 px-3 transition duration-200 focus-within:border-[#3B82F6]/70"><Icon name="Search" className="h-4 w-4 shrink-0 text-[#6B7280]" /><input value={symbol} onFocus={() => setSearchFocused(true)} onChange={(event) => setSymbol(event.target.value.toUpperCase())} className="h-10 min-w-0 w-full bg-transparent text-sm text-[#E5E7EB] outline-none placeholder:text-[#6B7280]" placeholder="Search symbol..." aria-label="Stock symbol" /></div><button type="submit" disabled={loading} className="hidden h-10 rounded-xl bg-[#3B82F6] px-4 text-sm font-semibold text-white transition duration-200 hover:bg-blue-500 active:scale-95 disabled:cursor-not-allowed disabled:opacity-60 sm:block">{loading ? "Analyzing" : "Analyze"}</button>{searchFocused && filteredResults.length > 0 && <div className="absolute left-0 top-12 z-50 w-[calc(100%-48px)] overflow-hidden rounded-xl border border-[#374151] bg-[#111827] p-1 shadow-2xl shadow-black/30">{filteredResults.map((item) => <button key={item} type="button" onMouseDown={() => requestAnalysis(item)} className="flex w-full items-center justify-between rounded-lg px-3 py-2 text-left text-sm text-[#E5E7EB] transition hover:bg-[#1F2937]"><span className="font-semibold">{item}</span><span className="text-xs text-[#9CA3AF]">Analyze</span></button>)}</div>}</form><div className="hidden items-center gap-2 rounded-lg border border-[#1F2937] bg-[#111827]/70 px-3 py-2 lg:flex"><span className="h-1.5 w-1.5 animate-pulse rounded-full bg-[#22C55E]" /><span className="text-xs text-[#9CA3AF]">S&P 500</span><span className="text-xs font-semibold text-[#22C55E]">+0.62%</span></div><button className="hidden rounded-lg border border-[#3B82F6]/40 bg-[#3B82F6]/10 px-3 py-2 text-xs font-semibold text-blue-200 transition duration-200 hover:bg-[#3B82F6]/20 active:scale-95 sm:block">Upgrade</button><button className="relative grid h-10 w-10 place-items-center rounded-xl text-[#9CA3AF] transition hover:bg-[#1F2937] hover:text-white active:scale-95" aria-label="Notifications"><Icon name="Bell" className="h-5 w-5" /><span className="absolute right-2 top-2 h-1.5 w-1.5 rounded-full bg-[#3B82F6]" /></button><div className="grid h-9 w-9 place-items-center rounded-full bg-gradient-to-br from-violet-400 to-fuchsia-600 text-xs font-bold text-white">AR</div></header>

      <main className="mx-auto max-w-[1680px] p-4 md:p-7"><div className="mb-7 flex flex-wrap items-end justify-between gap-3"><div><p className="text-xs font-semibold uppercase tracking-[0.18em] text-blue-300">Live workspace</p><h1 className="mt-1 text-2xl font-semibold tracking-tight text-[#E5E7EB] md:text-3xl">Trading Dashboard</h1></div><div className="flex items-center gap-3 text-right"><div><p className="text-sm font-semibold text-[#E5E7EB]">{result?.symbol || "Choose a symbol"}</p><p className="mt-1 text-xs text-[#9CA3AF]">Timeframe: {timeframe}</p></div></div></div>{result?.error && <div className="mb-5 rounded-xl border border-[#EF4444]/30 bg-[#EF4444]/10 px-4 py-3 text-sm text-[#FCA5A5]">{result.error}</div>}
        <div className="grid gap-5 xl:grid-cols-[minmax(0,1fr)_330px]"><Card className="min-w-0 p-4 md:p-5" hover={false}><div className="mb-3 flex items-center justify-between"><div><h2 className="font-semibold text-[#E5E7EB]">{result?.symbol || "Market chart"}</h2><p className="mt-1 text-xs text-[#9CA3AF]">Candles · SMA 20 · RSI signal markers</p></div>{result?.price && <p className="text-lg font-semibold text-[#E5E7EB]">${result.price}</p>}</div>{loading ? <div className="space-y-4"><Skeleton className="h-8 w-64" /><Skeleton className="h-[420px] w-full" /></div> : result?.chart?.length ? <TradingChart data={result.chart} selectedTimeframe={timeframe} onTimeframeChange={setTimeframe} /> : <div className="grid min-h-[470px] place-items-center rounded-xl border border-dashed border-[#374151] bg-[#0B0F14]/60 text-center"><div><div className="mx-auto mb-3 grid h-11 w-11 place-items-center rounded-xl bg-[#3B82F6]/10 text-blue-200"><Icon name="Markets" className="h-6 w-6" /></div><p className="font-medium text-[#E5E7EB]">Your chart will appear here</p><p className="mt-1 text-sm text-[#9CA3AF]">Search a symbol to begin analysis.</p></div></div>}</Card>
          <aside className="space-y-5"><SignalPanel result={result} loading={loading} /><AIInsights insights={insights} loading={loading} onRegenerate={() => requestAnalysis()} /><Watchlist activeSymbol={result?.symbol || symbol} onSelect={requestAnalysis} /></aside></div>
      </main>
    </div>
    <nav className="fixed inset-x-0 bottom-0 z-40 flex border-t border-[#1F2937] bg-[#111827]/95 px-2 py-2 backdrop-blur-xl md:hidden">{navigation.map((item) => <button key={item} onClick={() => setActiveNav(item)} className={`flex flex-1 flex-col items-center gap-1 rounded-lg py-1 text-[10px] transition ${activeNav === item ? "text-blue-300" : "text-[#9CA3AF]"}`}><Icon name={item} className="h-5 w-5" />{item}</button>)}</nav>
    {toast && <div className="fixed bottom-24 right-4 z-50 rounded-xl border border-[#22C55E]/30 bg-[#111827]/95 px-4 py-3 text-sm font-medium text-[#86EFAC] shadow-2xl backdrop-blur-xl md:bottom-6">✓ {toast}</div>}
  </div>;
}

export default App;
