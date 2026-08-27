export default function Ticker() {
  const items = [
    "AIRFARE MARKET PULSE",
    "APIx 108.4 ↑3.2%",
    "DEL → BOM ₹5,842 ↑6.8%",
    "DEL → BLR ₹6,930 ↓2.1%",
    "BOM → BLR ₹4,910 ↑1.7%",
  ];

  return (
    <div className="ticker">
      <div>
        {[...items, ...items].map((x, i) => (
          <span key={i}>
            <i />
            {x}
          </span>
        ))}
      </div>
    </div>
  );
}
