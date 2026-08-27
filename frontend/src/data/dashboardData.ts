export type Stat = {
  title: string;
  value: string;
  change: string;
  period: string;
  type: "blue" | "gray" | "green" | "orange";
};

export type TrendItem = {
  month: string;
  value: number;
};

export type TopRoute = {
  rank: string;
  route: string;
  city: string;
  fare: string;
  movement: string;
  observations: string;
};

export type CollectionItem = {
  name: string;
  type: string;
  records: string;
  status: "Active" | "Warning";
  initial: string;
};

export const dashboardStats: Stat[] = [
  {
    title: "OVERALL AIRFARE INDEX",
    value: "128.42",
    change: "+4.8%",
    period: "vs previous period",
    type: "blue",
  },
  {
    title: "AVERAGE DOMESTIC FARE",
    value: "₹5,840",
    change: "+3.2%",
    period: "month-on-month",
    type: "gray",
  },
  {
    title: "ACTIVE ROUTES",
    value: "86",
    change: "+6",
    period: "in current coverage",
    type: "green",
  },
  {
    title: "RECORDS COLLECTED",
    value: "1.24M",
    change: "+12.6%",
    period: "last 30 days",
    type: "orange",
  },
];

export const trendData: TrendItem[] = [
  { month: "Sep", value: 115.4 },
  { month: "Oct", value: 117.8 },
  { month: "Nov", value: 116.9 },
  { month: "Dec", value: 121.4 },
  { month: "Jan", value: 123.1 },
  { month: "Feb", value: 126.7 },
  { month: "Mar", value: 128.42 },
];

export const topRoutes: TopRoute[] = [
  {
    rank: "01",
    route: "DEL → BOM",
    city: "Delhi — Mumbai",
    fare: "₹4,850",
    movement: "+8.4%",
    observations: "18,420 obs.",
  },
  {
    rank: "02",
    route: "BOM → BLR",
    city: "Mumbai — Bengaluru",
    fare: "₹5,120",
    movement: "+5.2%",
    observations: "16,804 obs.",
  },
  {
    rank: "03",
    route: "DEL → BLR",
    city: "Delhi — Bengaluru",
    fare: "₹6,100",
    movement: "+3.7%",
    observations: "14,932 obs.",
  },
  {
    rank: "04",
    route: "HYD → DEL",
    city: "Hyderabad — Delhi",
    fare: "₹4,390",
    movement: "-1.4%",
    observations: "12,215 obs.",
  },
];

export const collectionStatus: CollectionItem[] = [
  {
    name: "IndiGo",
    type: "Airline",
    records: "426,812 records",
    status: "Active",
    initial: "I",
  },
  {
    name: "Air India",
    type: "Airline",
    records: "281,490 records",
    status: "Active",
    initial: "A",
  },
  {
    name: "Travel aggregator A",
    type: "OTA",
    records: "309,204 records",
    status: "Warning",
    initial: "T",
  },
  {
    name: "Travel aggregator B",
    type: "OTA",
    records: "225,180 records",
    status: "Active",
    initial: "T",
  },
];
