function Card({ children, className = "", hover = true }) {
  return (
    <section
      className={`rounded-xl border border-[#1F2937] bg-[#111827]/90 shadow-[0_12px_40px_rgba(0,0,0,0.18)] backdrop-blur-xl transition duration-200 ease-in-out ${hover ? "hover:-translate-y-0.5 hover:border-slate-600 hover:shadow-[0_18px_50px_rgba(0,0,0,0.24)]" : ""} ${className}`}
    >
      {children}
    </section>
  );
}

export default Card;
