export interface AddProductTestData {
  TestCaseID: string;
  Name: string;
  Description: string;
  Price: string;
  Brand: string;
  Category: string;
  ProductImage: string;
  Stock: string;
  LocationOffer: string;
  Rental: string;
}

export interface AdminTestConfig {
  testCaseIds?: string[];
  runAll?: boolean;
  testDataFile?: string;
  adminCredentials?: {
    email: string;
    password: string;
  };
}

export interface AdminTestResult {
  testCaseId: string;
  status: "passed" | "failed" | "skipped";
  errorMessage?: string;
  duration?: number;
  validationErrors?: Record<string, string[]>;
}

export interface NominalValues {
  name: string;
  description: string;
  price: string;
  brand: string;
  category: string;
  productImage: string;
  stock: string;
}
