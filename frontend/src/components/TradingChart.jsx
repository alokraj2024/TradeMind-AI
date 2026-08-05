import { useEffect, useRef, useState } from "react";
import { createChart } from "lightweight-charts";
import Skeleton from "./Skeleton";

const markerOptions = {
  BUY: { color: "#22C55E", position: "belowBar", shape: "arrowUp", size: 1 },
  "STRONG BUY": { color: "#86EFAC", position: "belowBar", shape: "arrowUp", size: 2 },
  SELL: { color: "#EF4444", position: "aboveBar", shape: "arrowDown", size: 1 },
  "STRONG SELL": { color: "#FCA5A5", position: "aboveBar", shape: "arrowDown", size: 2 },
};

const timeframes = ["1m", "5m", "15m", "1H", "1D"];

function TradingChart({ data, selectedTimeframe = "1D", onTimeframeChange }) {
  const containerRef = useRef(null);
  const shellRef = useRef(null);
  const [showSMA, setShowSMA] = useState(true);
  const [showRSI, setShowRSI] = useState(false);
  const [ready, setReady] = useState(false);

  useEffect(() => {
    const container = containerRef.current;
    if (!container || !data?.length) return undefined;
    setReady(false);

    const chart = createChart(container, {
      width: container.clientWidth,
      height: 420,
      layout: { background: { color: "#0B0F14" }, textColor: "#9CA3AF" },
      grid: { vertLines: { color: "#1F2937" }, horzLines: { color: "#1F2937" } },
      rightPriceScale: { borderColor: "#374151" },
      timeScale: { borderColor: "#374151", timeVisible: true, secondsVisible: false },
      crosshair: { vertLine: { color: "#4B5563" }, horzLine: { color: "#4B5563" } },
      handleScroll: { mouseWheel: true, pressedMouseMove: true, horzTouchDrag: true, vertTouchDrag: true },
      handleScale: { mouseWheel: true, pinch: true, axisPressedMouseMove: true },
    });

    const candleSeries = chart.addCandlestickSeries({
      upColor: "#22C55E", downColor: "#EF4444", borderVisible: false,
      wickUpColor: "#22C55E", wickDownColor: "#EF4444",
    });
    candleSeries.setData(data.map(({ time, open, high, low, close }) => ({ time, open, high, low, close })));

    if (showSMA) {
      const smaSeries = chart.addLineSeries({ color: "#60A5FA", lineWidth: 2, title: "SMA 20", lastValueVisible: false });
      smaSeries.setData(data.filter((candle) => candle.sma_20 !== null && candle.sma_20 !== undefined).map((candle) => ({ time: candle.time, value: candle.sma_20 })));
    }

    if (showRSI) {
      const rsiSeries = chart.addLineSeries({ color: "#C084FC", lineWidth: 1, title: "RSI", priceScaleId: "rsi", lastValueVisible: false });
      rsiSeries.setData(data.filter((candle) => candle.rsi !== null && candle.rsi !== undefined).map((candle) => ({ time: candle.time, value: candle.rsi })));
      chart.priceScale("rsi").applyOptions({ scaleMargins: { top: 0.76, bottom: 0.03 }, borderVisible: false });
    }

    candleSeries.setMarkers(data.filter((candle) => markerOptions[candle.signal]).map((candle) => ({ time: candle.time, ...markerOptions[candle.signal], text: candle.signal })));
    chart.timeScale().fitContent();
    setReady(true);

    const resizeObserver = new ResizeObserver(([entry]) => chart.applyOptions({ width: entry.contentRect.width }));
    resizeObserver.observe(container);
    return () => { resizeObserver.disconnect(); chart.remove(); };
  }, [data, showSMA, showRSI]);

  const enterFullscreen = () => shellRef.current?.requestFullscreen?.();
  const buttonClass = (active) => `rounded-md px-2.5 py-1.5 text-xs font-medium transition duration-200 ease-in-out active:scale-95 ${active ? "bg-[#3B82F6] text-white shadow-lg shadow-blue-500/20" : "text-[#9CA3AF] hover:bg-[#1F2937] hover:text-[#E5E7EB]"}`;

  return <div ref={shellRef} className="relative mt-4 w-full rounded-xl border border-[#1F2937] bg-[#0B0F14] p-2 transition duration-200 ease-in-out"><div className="flex flex-wrap items-center justify-between gap-2 border-b border-[#1F2937] px-2 pb-2"><div className="flex items-center gap-1 rounded-lg bg-[#111827] p-1">{timeframes.map((period) => <button key={period} onClick={() => onTimeframeChange?.(period)} className={buttonClass(selectedTimeframe === period)}>{period}</button>)}</div><div className="flex items-center gap-1"><button onClick={() => setShowSMA((value) => !value)} className={buttonClass(showSMA)}>SMA</button><button onClick={() => setShowRSI((value) => !value)} className={buttonClass(showRSI)}>RSI</button><button onClick={enterFullscreen} className={`${buttonClass(false)} ml-1 border border-[#374151]`} aria-label="Fullscreen chart">⛶</button></div></div><div className={`relative mt-2 transition-opacity duration-500 ${ready ? "opacity-100" : "opacity-0"}`}><div ref={containerRef} className="min-h-[420px] w-full touch-pan-x" /></div>{!ready && <div className="absolute inset-x-3 bottom-3 top-14 space-y-4"><Skeleton className="h-7 w-48" /><Skeleton className="h-[390px] w-full" /></div>}</div>;
}

export default TradingChart;
