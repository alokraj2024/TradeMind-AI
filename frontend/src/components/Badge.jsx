const variants = {
  success: "border-[#22C55E]/30 bg-[#22C55E]/10 text-[#86EFAC]",
  danger: "border-[#EF4444]/30 bg-[#EF4444]/10 text-[#FCA5A5]",
  warning: "border-amber-400/30 bg-amber-400/10 text-amber-200",
  info: "border-[#3B82F6]/30 bg-[#3B82F6]/10 text-blue-200",
  neutral: "border-[#374151] bg-[#1F2937] text-[#9CA3AF]",
};

function Badge({ children, variant = "neutral", className = "" }) {
  return <span className={`inline-flex items-center rounded-md border px-2.5 py-1 text-xs font-semibold tracking-wide ${variants[variant]} ${className}`}>{children}</span>;
}

export default Badge;
