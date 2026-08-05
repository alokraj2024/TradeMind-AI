function Skeleton({ className = "" }) {
  return <div className={`skeleton-shimmer rounded-lg bg-gradient-to-r from-[#1F2937] via-[#374151] to-[#1F2937] bg-[length:200%_100%] ${className}`} />;
}

export default Skeleton;
