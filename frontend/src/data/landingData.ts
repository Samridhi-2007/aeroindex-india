export type RouteData = {
  id: string;
  from: string;
  to: string;
  fare: number;
  change: number;
  apix: number;
  apixChange: number;
  volatility: string;
  confidence: number;
  range: string;
  points: number[];
  expected: number[];
};

export const routes: RouteData[] = [
  {
    id: "DEL-BOM",
    from: "DEL",
    to: "BOM",
    fare: 5842,
    change: 6.8,
    apix: 112.6,
    apixChange: 3.1,
    volatility: "Moderate",
    confidence: 92,
    range: "₹5.2K – ₹6.1K",
    points: [5200, 5360, 5290, 5480, 5540, 5720, 5842],
    expected: [5100, 5200, 5280, 5360, 5450, 5540, 5620],
  },
  {
    id: "DEL-BLR",
    from: "DEL",
    to: "BLR",
    fare: 6930,
    change: -2.1,
    apix: 104.2,
    apixChange: -1.3,
    volatility: "Low",
    confidence: 89,
    range: "₹6.4K – ₹7.2K",
    points: [7240, 7180, 7070, 7120, 6990, 7040, 6930],
    expected: [6900, 6910, 6920, 6930, 6940, 6950, 6960],
  },
  {
    id: "BOM-BLR",
    from: "BOM",
    to: "BLR",
    fare: 4910,
    change: 1.7,
    apix: 107.8,
    apixChange: 0.8,
    volatility: "Low",
    confidence: 95,
    range: "₹4.6K – ₹5.2K",
    points: [4680, 4730, 4710, 4790, 4850, 4820, 4910],
    expected: [4700, 4740, 4770, 4800, 4830, 4860, 4890],
  },
  {
    id: "BLR-HYD",
    from: "BLR",
    to: "HYD",
    fare: 3840,
    change: 4.2,
    apix: 109.1,
    apixChange: 2.2,
    volatility: "Moderate",
    confidence: 91,
    range: "₹3.5K – ₹4.1K",
    points: [3510, 3480, 3620, 3590, 3700, 3750, 3840],
    expected: [3500, 3540, 3580, 3620, 3660, 3700, 3740],
  },
  {
    id: "MAA-DEL",
    from: "MAA",
    to: "DEL",
    fare: 7120,
    change: 3.9,
    apix: 111.3,
    apixChange: 2.6,
    volatility: "High",
    confidence: 86,
    range: "₹6.5K – ₹7.4K",
    points: [6540, 6610, 6730, 6680, 6890, 7010, 7120],
    expected: [6500, 6590, 6670, 6760, 6840, 6930, 7010],
  },
  {
    id: "DEL-CCU",
    from: "DEL",
    to: "CCU",
    fare: 6215,
    change: 3.4,
    apix: 110.4,
    apixChange: 1.9,
    volatility: "Moderate",
    confidence: 90,
    range: "₹5.8K – ₹6.6K",
    points: [5790, 5880, 5840, 5960, 6030, 6140, 6215],
    expected: [5800, 5870, 5940, 6010, 6080, 6150, 6220],
  },
];

export const airportNames: Record<string, string> = {
  DEL: "Delhi",
  BOM: "Mumbai",
  BLR: "Bengaluru",
  HYD: "Hyderabad",
  MAA: "Chennai",
  CCU: "Kolkata",
};

export const airports = Object.keys(airportNames);

export const windows = ["T+1", "T+7", "T+15", "T+30", "T+45"];

export const windowCopy: Record<string, string> = {
  "T+1": "Booking tomorrow",
  "T+7": "Booking 7 days ahead",
  "T+15": "Booking 15 days ahead",
  "T+30": "Booking one month ahead",
  "T+45": "Booking 45 days ahead",
};

export const stages = [
  [
    "Database",
    "Data Collection",
    "Airlines and OTAs are tracked across major Indian city pairs.",
  ],
  [
    "ShieldCheck",
    "Normalization",
    "Fare quotes are cleaned and standardized for true comparability.",
  ],
  [
    "BarChart3",
    "Index Computation",
    "Daily, weekly, and monthly signals are aggregated into APIx.",
  ],
  [
    "Sparkles",
    "Insight Layer",
    "Trends, anomalies, volatility, and booking-window movement surface.",
  ],
];

export const signals = [
  [
    "Activity",
    "Fare anomaly detected",
    "DEL → BLR",
    "31% above expected range",
    "₹9,240",
    "Confidence 92%",
    "anomaly",
  ],
  [
    "TrendingUp",
    "Highest weekly increase",
    "DEL → BOM",
    "Up 6.8% this week",
    "₹5,842",
    "Momentum rising",
    "positive",
  ],
  [
    "Gauge",
    "Most stable route",
    "BOM → BLR",
    "Variance below 3%",
    "₹4,910",
    "Stable signal",
    "stable",
  ],
  [
    "RefreshCw",
    "Strongest booking-window shift",
    "MAA → DEL",
    "Demand moved forward",
    "T+15",
    "Observed today",
    "warning",
  ],
];

export const chips = [
  ["Plane", "Airlines", "Scheduled airline observations"],
  ["Search", "OTAs", "Representative market quotes"],
  ["RouteIcon", "Route Basket", "Major Indian corridors"],
  ["Gauge", "Booking Windows", "T+1 through T+45"],
  ["RefreshCw", "Daily Refresh", "Continuously refreshed signals"],
  [
    "CheckCircle2",
    "Quality Validation",
    "Cross-source consistency and anomaly checks",
  ],
];
