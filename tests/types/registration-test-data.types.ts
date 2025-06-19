// tests/types/registration-test-data.types.ts

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

export interface RegistrationTestConfig {
  testCaseIds?: string[];
  runAll?: boolean;
  testDataFile?: string;
  // Exclude configuration (only applies when runAll is true)
  excludeTestCases?: string[];
  excludeByPrefix?: string[];
  excludeBySuffix?: string[];
}

export interface RegistrationTestResult {
  testCaseId: string;
  status: "passed" | "failed" | "skipped";
  errorMessage?: string;
  duration?: number;
}

export interface RegistrationSubmissionResult {
  isSuccess: boolean;
  hasValidationErrors: boolean;
  hasServerError: boolean;
  validationErrors: Record<string, string[]>;
  serverError?: string;
  currentUrl: string;
  redirected: boolean;
}
