export interface RegistrationTestData {
  TestCaseID: string;
  FirstName: string;
  LastName: string;
  DOB: string;
  Street: string;
  City: string;
  State: string;
  Country: string;
  PostalCode: string;
  Phone: string;
  Email: string;
  Password: string;
}

export interface TestConfig {
  testCaseIds?: string[];
  runAll?: boolean;
  testDataFile?: string;
  // Exclude configuration (only applies when runAll is true)
  excludeTestCases?: string[];
  excludeByPrefix?: string[];
  excludeBySuffix?: string[];
}

export interface TestResult {
  testCaseId: string;
  status: "passed" | "failed" | "skipped";
  errorMessage?: string;
  duration?: number;
}

export interface SubmissionResult {
  isSuccess: boolean;
  hasValidationErrors: boolean;
  hasServerError: boolean;
  validationErrors: Record<string, string[]>;
  serverError?: string;
  currentUrl: string;
  redirected: boolean;
}
