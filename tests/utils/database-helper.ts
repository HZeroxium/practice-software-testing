import { exec } from "child_process";
import { promisify } from "util";

const execAsync = promisify(exec);

export class DatabaseHelper {
  private static readonly DOCKER_COMPOSE_PATH =
    process.env.DOCKER_COMPOSE_PATH || ".";
  private static readonly DB_CONTAINER_NAME = "laravel-api";
  private static resetInProgress = false;
  private static resetQueue: Array<() => void> = [];

  /**
   * Reset database to fresh state with seeded data
   * This preserves the default accounts while clearing user-generated data
   */
  static async resetDatabase(): Promise<void> {
    // Handle concurrent reset requests
    if (this.resetInProgress) {
      console.log("🔄 Database reset already in progress, waiting...");
      return new Promise((resolve) => {
        this.resetQueue.push(resolve);
      });
    }

    this.resetInProgress = true;

    try {
      console.log("🔄 Resetting database to fresh state...");

      // First, ensure containers are running
      await this.ensureContainersRunning();

      // Check if database is accessible before reset
      const isAccessible = await this.isDatabaseAccessible();
      if (!isAccessible) {
        console.log(
          "⚠️ Database not accessible, waiting for initialization..."
        );
        await this.waitForDatabaseReady(30000); // Wait up to 30 seconds
      }

      const command = `docker-compose exec -T ${this.DB_CONTAINER_NAME} php artisan migrate:fresh --seed`;

      const { stdout, stderr } = await execAsync(command, {
        cwd: this.DOCKER_COMPOSE_PATH,
        timeout: 120000, // Increased timeout to 2 minutes
      });

      // Filter out known warnings that don't affect functionality
      const filteredStderr = this.filterKnownWarnings(stderr);

      if (filteredStderr) {
        console.warn("⚠️ Database reset warnings:", filteredStderr);
      }

      console.log("✅ Database reset completed successfully");

      // Wait for database to be fully ready
      await this.waitForDatabaseReady();

      // Resolve any queued reset requests
      this.resolveQueuedResets();
    } catch (error) {
      console.error("❌ Failed to reset database:", error);

      // Try alternative reset approach
      try {
        console.log("🔄 Attempting alternative database reset...");
        await this.alternativeResetDatabase();
        console.log("✅ Alternative database reset completed");
        this.resolveQueuedResets();
      } catch (alternativeError) {
        this.rejectQueuedResets(error);
        throw new Error(
          `Database reset failed: ${
            error instanceof Error ? error.message : String(error)
          }`
        );
      }
    } finally {
      this.resetInProgress = false;
    }
  }

  /**
   * Alternative database reset method for when primary method fails
   */
  private static async alternativeResetDatabase(): Promise<void> {
    try {
      // First try to run migrations without dropping tables
      const migrateCommand = `docker-compose exec -T ${this.DB_CONTAINER_NAME} php artisan migrate --force`;
      await execAsync(migrateCommand, {
        cwd: this.DOCKER_COMPOSE_PATH,
        timeout: 60000,
      });

      // Then seed the database
      const seedCommand = `docker-compose exec -T ${this.DB_CONTAINER_NAME} php artisan db:seed --force`;
      await execAsync(seedCommand, {
        cwd: this.DOCKER_COMPOSE_PATH,
        timeout: 60000,
      });
    } catch (error) {
      console.error("❌ Alternative database reset also failed:", error);
      throw error;
    }
  }

  /**
   * Filter out known Docker Compose warnings that don't affect functionality
   */
  private static filterKnownWarnings(stderr: string): string {
    if (!stderr) return "";

    const knownWarnings = [
      /The "DISABLE_LOGGING" variable is not set/i,
      /the attribute `version` is obsolete/i,
      /PHP Startup: Unable to load dynamic library 'ffi/i,
    ];

    const lines = stderr.split("\n");
    const filteredLines = lines.filter((line) => {
      return !knownWarnings.some((pattern) => pattern.test(line));
    });

    return filteredLines.join("\n").trim();
  }

  /**
   * Resolve queued reset requests
   */
  private static resolveQueuedResets(): void {
    while (this.resetQueue.length > 0) {
      const resolve = this.resetQueue.shift();
      if (resolve) resolve();
    }
  }

  /**
   * Reject queued reset requests with error
   */
  private static rejectQueuedResets(error: any): void {
    while (this.resetQueue.length > 0) {
      const resolve = this.resetQueue.shift();
      if (resolve) resolve(); // Still resolve to avoid hanging tests
    }
  }

  /**
   * Check if database is accessible (different from ready check)
   */
  static async isDatabaseAccessible(): Promise<boolean> {
    try {
      const command = `docker-compose exec -T ${this.DB_CONTAINER_NAME} php artisan tinker --execute="DB::connection()->getPdo();"`;
      await execAsync(command, {
        cwd: this.DOCKER_COMPOSE_PATH,
        timeout: 10000,
      });
      return true;
    } catch {
      return false;
    }
  }

  /**
   * Check if database is ready and accessible
   */
  static async isDatabaseReady(): Promise<boolean> {
    try {
      const command = `docker-compose exec -T ${this.DB_CONTAINER_NAME} php artisan migrate:status`;
      await execAsync(command, {
        cwd: this.DOCKER_COMPOSE_PATH,
        timeout: 10000,
      });
      return true;
    } catch {
      return false;
    }
  }

  /**
   * Wait for database to be ready after reset
   */
  private static async waitForDatabaseReady(
    maxWaitTime = 15000
  ): Promise<void> {
    const startTime = Date.now();
    const checkInterval = 1000; // Check every 1 second

    console.log("⏳ Waiting for database to be ready...");

    while (Date.now() - startTime < maxWaitTime) {
      if (await this.isDatabaseReady()) {
        console.log("✅ Database is ready");
        return;
      }
      console.log("⏳ Database not ready yet, waiting...");
      await new Promise((resolve) => setTimeout(resolve, checkInterval));
    }

    console.warn("⚠️ Database readiness check timed out, proceeding anyway");
  }

  /**
   * Clean up specific user data while preserving default accounts
   */
  static async cleanupUserData(
    excludeEmails: string[] = [
      "admin@practicesoftwaretesting.com",
      "customer@practicesoftwaretesting.com",
      "customer2@practicesoftwaretesting.com",
    ]
  ): Promise<void> {
    try {
      console.log("🧹 Cleaning up user data...");

      const emailList = excludeEmails.map((email) => `'${email}'`).join(",");
      const command = `docker-compose exec -T ${this.DB_CONTAINER_NAME} php artisan tinker --execute="DB::table('users')->whereNotIn('email', [${emailList}])->delete();"`;

      await execAsync(command, {
        cwd: this.DOCKER_COMPOSE_PATH,
        timeout: 30000,
      });

      console.log("✅ User data cleanup completed");
    } catch (error) {
      console.error("❌ Failed to cleanup user data:", error);
      throw error;
    }
  }

  /**
   * Execute custom database commands
   */
  static async executeCommand(artisanCommand: string): Promise<string> {
    try {
      const command = `docker-compose exec -T ${this.DB_CONTAINER_NAME} php artisan ${artisanCommand}`;
      const { stdout } = await execAsync(command, {
        cwd: this.DOCKER_COMPOSE_PATH,
        timeout: 30000,
      });
      return stdout;
    } catch (error) {
      console.error(`❌ Failed to execute command: ${artisanCommand}`, error);
      throw error;
    }
  }

  /**
   * Get database connection info for GUI tools
   */
  static getDatabaseConnectionInfo(): {
    host: string;
    port: number;
    database: string;
    username: string;
    password: string;
    phpMyAdminUrl: string;
  } {
    return {
      host: "localhost",
      port: 3306,
      database: "practicesoftwaretesting",
      username: "root",
      password: "root",
      phpMyAdminUrl: "http://localhost:8000",
    };
  }

  /**
   * Check if Docker containers are running
   */
  static async areContainersRunning(): Promise<boolean> {
    try {
      const command = 'docker-compose ps --services --filter "status=running"';
      const { stdout } = await execAsync(command, {
        cwd: this.DOCKER_COMPOSE_PATH,
        timeout: 10000,
      });

      return stdout.includes(this.DB_CONTAINER_NAME);
    } catch {
      return false;
    }
  }

  /**
   * Start Docker containers if not running
   */
  static async ensureContainersRunning(): Promise<void> {
    if (!(await this.areContainersRunning())) {
      console.log("🐳 Starting Docker containers...");
      try {
        await execAsync("docker-compose up -d", {
          cwd: this.DOCKER_COMPOSE_PATH,
          timeout: 180000, // 3 minutes for container startup
        });

        // Wait for services to be fully ready
        console.log("⏳ Waiting for services to initialize...");
        await new Promise((resolve) => setTimeout(resolve, 15000)); // Wait 15 seconds

        // Verify database container is responsive
        await this.waitForDatabaseReady(30000);

        console.log("✅ Docker containers started successfully");
      } catch (error) {
        throw new Error(`Failed to start Docker containers: ${error}`);
      }
    } else {
      console.log("✅ Docker containers are already running");
    }
  }
}
