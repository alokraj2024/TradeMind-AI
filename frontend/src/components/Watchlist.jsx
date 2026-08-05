import Card from "./Card";

const watchlist = [
  { symbol: "AAPL", name: "Apple Inc.", price: "212.10", change: "+1.24%" },
  { symbol: "NVDA", name: "NVIDIA", price: "184.66", change: "+3.89%" },
  { symbol: "MSFT", name: "Microsoft", price: "514.78", change: "+0.42%" },
  { symbol: "TSLA", name: "Tesla", price: "329.12", change: "-1.18%" },
];

function Watchlist({ activeSymbol, onSelect }) {
  return (
    <Card className="overflow-hidden" hover={false}>
      <div className="flex items-center justify-between border-b border-[#1F2937] px-5 py-4"><div><h2 className="text-sm font-semibold text-[#E5E7EB]">Watchlist</h2><p className="mt-0.5 text-xs text-[#9CA3AF]">Major movers</p></div><button className="rounded-lg border border-[#374151] px-2.5 py-1.5 text-xs font-medium text-[#E5E7EB] transition duration-200 hover:border-[#3B82F6] hover:bg-[#3B82F6]/10 active:scale-95">+ Add Symbol</button></div>
      <div className="divide-y divide-[#1F2937]">
        {watchlist.map((item) => {
          const positive = item.change.startsWith("+");
          const active = activeSymbol === item.symbol;
          return <button key={item.symbol} onClick={() => onSelect(item.symbol)} className={`flex w-full items-center justify-between px-5 py-3 text-left transition duration-200 hover:bg-[#1F2937]/70 active:scale-[0.99] ${active ? "bg-[#3B82F6]/10" : ""}`}><div><p className="text-sm font-semibold text-[#E5E7EB]">{item.symbol}</p><p className="mt-0.5 text-xs text-[#9CA3AF]">{item.name}</p></div><div className="text-right"><p className="text-sm font-medium text-[#E5E7EB]">${item.price}</p><p className={`mt-0.5 text-xs font-medium ${positive ? "text-[#22C55E]" : "text-[#EF4444]"}`}>{item.change}</p></div></button>;
        })}
      </div>
    </Card>
  );
}

export default Watchlist;
