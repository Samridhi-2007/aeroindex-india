export type RouteStatus = "Active" | "Watch" | "Low Confidence";

export type BookingWindow = "T+1" | "T+7" | "T+15" | "T+30" | "T+45";

export interface RouteForecast {
  horizon: BookingWindow;
  averageFare: number;
  changePercent: number;
}

export interface RouteData {
  id: string;

  origin: {
    code: string;
    name: string;
  };

  destination: {
    code: string;
    name: string;
  };

  carrier: string;

  bookingWindow: BookingWindow;

  weight: number;

  averageFare: number;

  baseFare: number;

  inflationPercent: number;

  apix: number;

  apixContribution: number;

  weeklyChange: number;

  confidence: number;

  status: RouteStatus;

  forecast: RouteForecast[];
}

export const routesData: RouteData[] = [
  {
    id: "DEL-BOM",
    origin: {
      code: "DEL",
      name: "Delhi",
    },
    destination: {
      code: "BOM",
      name: "Mumbai",
    },
    carrier: "IndiGo",
    bookingWindow: "T+7",
    weight: 12.4,
    averageFare: 6240,
    baseFare: 5820,
    inflationPercent: 7.2,
    apix: 108.4,
    apixContribution: 13.8,
    weeklyChange: 4.2,
    confidence: 94,
    status: "Active",
    forecast: [
      { horizon: "T+1", averageFare: 6280, changePercent: 0.6 },
      { horizon: "T+7", averageFare: 6410, changePercent: 2.7 },
      { horizon: "T+15", averageFare: 6520, changePercent: 4.5 },
      { horizon: "T+30", averageFare: 6680, changePercent: 7.1 },
      { horizon: "T+45", averageFare: 6790, changePercent: 8.8 },
    ],
  },

  {
    id: "BOM-DEL",
    origin: {
      code: "BOM",
      name: "Mumbai",
    },
    destination: {
      code: "DEL",
      name: "Delhi",
    },
    carrier: "Air India",
    bookingWindow: "T+7",
    weight: 11.8,
    averageFare: 5980,
    baseFare: 5660,
    inflationPercent: 5.7,
    apix: 104.7,
    apixContribution: 12.3,
    weeklyChange: 2.1,
    confidence: 92,
    status: "Active",
    forecast: [
      { horizon: "T+1", averageFare: 6020, changePercent: 0.7 },
      { horizon: "T+7", averageFare: 6110, changePercent: 2.2 },
      { horizon: "T+15", averageFare: 6200, changePercent: 3.7 },
      { horizon: "T+30", averageFare: 6340, changePercent: 6.0 },
      { horizon: "T+45", averageFare: 6420, changePercent: 7.4 },
    ],
  },

  {
    id: "DEL-BLR",
    origin: {
      code: "DEL",
      name: "Delhi",
    },
    destination: {
      code: "BLR",
      name: "Bengaluru",
    },
    carrier: "IndiGo",
    bookingWindow: "T+15",
    weight: 9.7,
    averageFare: 7120,
    baseFare: 6670,
    inflationPercent: 6.7,
    apix: 112.8,
    apixContribution: 10.9,
    weeklyChange: 6.8,
    confidence: 89,
    status: "Watch",
    forecast: [
      { horizon: "T+1", averageFare: 7180, changePercent: 0.8 },
      { horizon: "T+7", averageFare: 7340, changePercent: 3.1 },
      { horizon: "T+15", averageFare: 7480, changePercent: 5.1 },
      { horizon: "T+30", averageFare: 7650, changePercent: 7.5 },
      { horizon: "T+45", averageFare: 7810, changePercent: 9.7 },
    ],
  },

  {
    id: "BLR-DEL",
    origin: {
      code: "BLR",
      name: "Bengaluru",
    },
    destination: {
      code: "DEL",
      name: "Delhi",
    },
    carrier: "Vistara",
    bookingWindow: "T+7",
    weight: 9.2,
    averageFare: 6840,
    baseFare: 6510,
    inflationPercent: 5.1,
    apix: 109.3,
    apixContribution: 10.1,
    weeklyChange: -1.4,
    confidence: 95,
    status: "Active",
    forecast: [
      { horizon: "T+1", averageFare: 6810, changePercent: -0.4 },
      { horizon: "T+7", averageFare: 6760, changePercent: -1.2 },
      { horizon: "T+15", averageFare: 6820, changePercent: -0.3 },
      { horizon: "T+30", averageFare: 6940, changePercent: 1.5 },
      { horizon: "T+45", averageFare: 7050, changePercent: 3.1 },
    ],
  },

  {
    id: "DEL-HYD",
    origin: {
      code: "DEL",
      name: "Delhi",
    },
    destination: {
      code: "HYD",
      name: "Hyderabad",
    },
    carrier: "IndiGo",
    bookingWindow: "T+30",
    weight: 7.6,
    averageFare: 5430,
    baseFare: 5210,
    inflationPercent: 4.2,
    apix: 101.6,
    apixContribution: 7.7,
    weeklyChange: 0.8,
    confidence: 91,
    status: "Active",
    forecast: [
      { horizon: "T+1", averageFare: 5460, changePercent: 0.5 },
      { horizon: "T+7", averageFare: 5510, changePercent: 1.5 },
      { horizon: "T+15", averageFare: 5580, changePercent: 2.8 },
      { horizon: "T+30", averageFare: 5640, changePercent: 3.9 },
      { horizon: "T+45", averageFare: 5720, changePercent: 5.3 },
    ],
  },

  {
    id: "BOM-BLR",
    origin: {
      code: "BOM",
      name: "Mumbai",
    },
    destination: {
      code: "BLR",
      name: "Bengaluru",
    },
    carrier: "Akasa Air",
    bookingWindow: "T+15",
    weight: 6.9,
    averageFare: 4780,
    baseFare: 4610,
    inflationPercent: 3.7,
    apix: 98.9,
    apixContribution: 6.4,
    weeklyChange: -2.3,
    confidence: 87,
    status: "Watch",
    forecast: [
      { horizon: "T+1", averageFare: 4750, changePercent: -0.6 },
      { horizon: "T+7", averageFare: 4690, changePercent: -1.9 },
      { horizon: "T+15", averageFare: 4720, changePercent: -1.3 },
      { horizon: "T+30", averageFare: 4810, changePercent: 0.6 },
      { horizon: "T+45", averageFare: 4890, changePercent: 2.3 },
    ],
  },

  {
    id: "MAA-DEL",
    origin: {
      code: "MAA",
      name: "Chennai",
    },
    destination: {
      code: "DEL",
      name: "Delhi",
    },
    carrier: "Air India",
    bookingWindow: "T+30",
    weight: 5.8,
    averageFare: 7310,
    baseFare: 6920,
    inflationPercent: 5.6,
    apix: 107.5,
    apixContribution: 6.2,
    weeklyChange: 3.6,
    confidence: 90,
    status: "Active",
    forecast: [
      { horizon: "T+1", averageFare: 7350, changePercent: 0.5 },
      { horizon: "T+7", averageFare: 7440, changePercent: 1.8 },
      { horizon: "T+15", averageFare: 7560, changePercent: 3.4 },
      { horizon: "T+30", averageFare: 7690, changePercent: 5.2 },
      { horizon: "T+45", averageFare: 7810, changePercent: 6.8 },
    ],
  },

  {
    id: "CCU-BOM",
    origin: {
      code: "CCU",
      name: "Kolkata",
    },
    destination: {
      code: "BOM",
      name: "Mumbai",
    },
    carrier: "IndiGo",
    bookingWindow: "T+45",
    weight: 5.1,
    averageFare: 6420,
    baseFare: 6120,
    inflationPercent: 4.9,
    apix: 103.8,
    apixContribution: 5.3,
    weeklyChange: 1.9,
    confidence: 84,
    status: "Low Confidence",
    forecast: [
      { horizon: "T+1", averageFare: 6460, changePercent: 0.6 },
      { horizon: "T+7", averageFare: 6530, changePercent: 1.7 },
      { horizon: "T+15", averageFare: 6640, changePercent: 3.4 },
      { horizon: "T+30", averageFare: 6760, changePercent: 5.3 },
      { horizon: "T+45", averageFare: 6890, changePercent: 7.3 },
    ],
  },
];
