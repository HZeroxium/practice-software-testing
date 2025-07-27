-- ============================================================
-- SQL INSERT Script for categories table
-- ============================================================
-- Generated: 2025-07-21T20:30:18.733874
-- Database: MYSQL
-- Records: 10
-- Generator: Faker Data Generator v2.0
-- ============================================================

START TRANSACTION;

INSERT INTO `categories` (`id`, `name`, `slug`, `parent_id`, `created_at`, `updated_at`)
VALUES
  ('01K0PJSFZ0MFNRBZN52E21QFG1', 'Hand Tools', 'hand-tools', NULL, '2025-07-21 13:29:24', '2025-07-21 13:29:24'),
  ('01K0PJSFZ0ENY24ARKYMVWNDWA', 'Power Tools', 'power-tools', NULL, '2025-07-21 13:29:24', '2025-07-21 13:29:24'),
  ('01K0PJSFZ0CXM2CDAYBEAF8SHF', 'Fasteners & Hardware', 'fasteners-hardware', NULL, '2025-07-21 13:29:24', '2025-07-21 13:29:24'),
  ('01K0PJSFZ0DC8ZVXEAJTMEPS5H', 'Safety Equipment', 'safety-equipment', NULL, '2025-07-21 13:29:24', '2025-07-21 13:29:24'),
  ('01K0PJSFZ072BANDRWCP0ZX3XS', 'Storage & Organization', 'storage-organization', NULL, '2025-07-21 13:29:24', '2025-07-21 13:29:24'),
  ('01K0PJSFZ0VSQEJ2S1AT2H3X70', 'Electrical', 'electrical', NULL, '2025-07-21 13:29:24', '2025-07-21 13:29:24'),
  ('01K0PJSFZ0TCGZ78BVXSQZ4X2B', 'Plumbing', 'plumbing', NULL, '2025-07-21 13:29:24', '2025-07-21 13:29:24'),
  ('01K0PJSFZ016YYNT6W1TQVAGDN', 'Garden & Outdoor', 'garden-outdoor', NULL, '2025-07-21 13:29:24', '2025-07-21 13:29:24'),
  ('01K0PJSFZ07T69CWG8DFZAMZ77', 'Automotive', 'automotive', NULL, '2025-07-21 13:29:24', '2025-07-21 13:29:24'),
  ('01K0PJSFZ032Q1JEF0Y4P95Y2Y', 'HVAC', 'hvac', NULL, '2025-07-21 13:29:24', '2025-07-21 13:29:24')
ON DUPLICATE KEY UPDATE
  `name` = VALUES(`name`),
  `slug` = VALUES(`slug`),
  `parent_id` = VALUES(`parent_id`),
  `updated_at` = VALUES(`updated_at`)
;

COMMIT;

-- ============================================================
-- Script completed successfully
-- Total records inserted: 10
-- ============================================================