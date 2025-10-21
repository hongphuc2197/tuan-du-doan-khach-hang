// Dữ liệu mẫu cho 576 sinh viên - khách hàng mua sách công nghệ giáo dục
export const mockCustomers = [
  {
    ID: 1,
    Age: 20,
    Income: 3000000,
    Recency: 15,
    TotalSpent: 450000,
    AvgPurchaseValue: 150000,
    PredictionProbability: 0.85,
    MntWines: 150000, // Công nghệ giáo dục
    MntFruits: 180000, // Phương pháp giảng dạy
    MntMeatProducts: 120000, // Công nghệ thông tin
    MntFishProducts: 95000, // Thiết kế web
    MntSweetProducts: 130000, // Lập trình
    MntGoldProds: 140000, // Nghiên cứu khoa học
    NumWebPurchases: 4,
    NumCatalogPurchases: 0,
    NumStorePurchases: 1,
    NumDealsPurchases: 1,
    NumWebVisitsMonth: 8,
    Kidhome: 0,
    Teenhome: 0,
    Education: 'Basic',
    Marital_Status: 'Single'
  },
  {
    ID: 2,
    Age: 22,
    Income: 2500000,
    Recency: 25,
    TotalSpent: 320000,
    AvgPurchaseValue: 160000,
    PredictionProbability: 0.72,
    MntWines: 120000,
    MntFruits: 150000,
    MntMeatProducts: 100000,
    MntFishProducts: 80000,
    MntSweetProducts: 110000,
    MntGoldProds: 120000,
    NumWebPurchases: 3,
    NumCatalogPurchases: 0,
    NumStorePurchases: 1,
    NumDealsPurchases: 2,
    NumWebVisitsMonth: 6,
    Kidhome: 0,
    Teenhome: 0,
    Education: 'Basic',
    Marital_Status: 'Single'
  },
  {
    ID: 3,
    Age: 24,
    Income: 4500000,
    Recency: 5,
    TotalSpent: 680000,
    AvgPurchaseValue: 170000,
    PredictionProbability: 0.95,
    MntWines: 200000,
    MntFruits: 220000,
    MntMeatProducts: 180000,
    MntFishProducts: 150000,
    MntSweetProducts: 190000,
    MntGoldProds: 200000,
    NumWebPurchases: 6,
    NumCatalogPurchases: 0,
    NumStorePurchases: 2,
    NumDealsPurchases: 1,
    NumWebVisitsMonth: 12,
    Kidhome: 0,
    Teenhome: 0,
    Education: 'Basic',
    Marital_Status: 'Single'
  },
  {
    ID: 4,
    Age: 19,
    Income: 1500000,
    Recency: 40,
    TotalSpent: 180000,
    AvgPurchaseValue: 90000,
    PredictionProbability: 0.45,
    MntWines: 80000,
    MntFruits: 90000,
    MntMeatProducts: 70000,
    MntFishProducts: 60000,
    MntSweetProducts: 75000,
    MntGoldProds: 85000,
    NumWebPurchases: 2,
    NumCatalogPurchases: 0,
    NumStorePurchases: 0,
    NumDealsPurchases: 3,
    NumWebVisitsMonth: 4,
    Kidhome: 0,
    Teenhome: 0,
    Education: 'Basic',
    Marital_Status: 'Single'
  },
  {
    ID: 5,
    Age: 23,
    Income: 3500000,
    Recency: 10,
    TotalSpent: 520000,
    AvgPurchaseValue: 173000,
    PredictionProbability: 0.88,
    MntWines: 170000,
    MntFruits: 190000,
    MntMeatProducts: 150000,
    MntFishProducts: 120000,
    MntSweetProducts: 160000,
    MntGoldProds: 170000,
    NumWebPurchases: 5,
    NumCatalogPurchases: 0,
    NumStorePurchases: 1,
    NumDealsPurchases: 1,
    NumWebVisitsMonth: 9,
    Kidhome: 0,
    Teenhome: 0,
    Education: 'Basic',
    Marital_Status: 'Single'
  }
];

export const mockAnalytics = {
  potentialCustomers: 312,
  nonPotentialCustomers: 264,
  demographics: {
    ageSegments: [
      { name: '18-20', count: 210 },
      { name: '21-23', count: 232 },
      { name: '24-25', count: 72 },
      { name: '26-28', count: 45 },
      { name: '29+', count: 17 }
    ],
    education: [
      { Education: 'Basic', potential_rate: 52.5 },
      { Education: 'Graduation', potential_rate: 58.4 },
      { Education: 'Master', potential_rate: 80.0 }
    ],
    income: [
      { Income: 'Low (1-2M)', potential_rate: 35.2 },
      { Income: 'Medium (2-4M)', potential_rate: 68.5 },
      { Income: 'High (4M+)', potential_rate: 82.3 }
    ]
  },
  spending: {
    byProduct: {
      'Công nghệ giáo dục': { mean: 150000, median: 120000, max: 300000 },
      'Phương pháp giảng dạy': { mean: 180000, median: 150000, max: 350000 },
      'Công nghệ thông tin': { mean: 120000, median: 100000, max: 250000 },
      'Thiết kế web': { mean: 95000, median: 80000, max: 200000 },
      'Lập trình': { mean: 130000, median: 110000, max: 280000 },
      'Nghiên cứu khoa học': { mean: 140000, median: 120000, max: 300000 }
    },
    byChannel: {
      'Mua sách online': { mean: 4.2, median: 3.5, max: 8 },
      'Mua sách qua catalog': { mean: 2.1, median: 1.8, max: 5 },
      'Mua sách tại cửa hàng': { mean: 3.8, median: 3.2, max: 7 },
      'Truy cập website tháng': { mean: 6.5, median: 5.8, max: 15 }
    }
  },
  interactions: {
    'Số lần mua hàng giảm giá': { mean: 2.1, median: 1.8, max: 5 },
    'Số ngày từ lần mua cuối': { mean: 30.5, median: 25.2, max: 90 },
    'Số con nhỏ': { mean: 0.3, median: 0, max: 3 },
    'Số con tuổi teen': { mean: 0.2, median: 0, max: 2 }
  }
};