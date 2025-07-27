-- ============================================================
-- SQL INSERT Script for categories table
-- ============================================================
-- Generated: 2025-07-20T08:16:32.800Z
-- Database: MYSQL
-- Records: 10
-- Generator: Mockaroo Categories Data Generator v2.0
-- ============================================================

START TRANSACTION;

INSERT INTO `categories` (`id`, `name`, `slug`, `parent_id`, `created_at`, `updated_at`)
VALUES
  ('MDBEKOAJSFOQKFXO', 'Hand Tools', 'hand-tools', NULL, '2024-04-17 02:27:01', '2024-04-17 02:27:01'),
  ('MDBEKOAJJE8UGA55', 'Power Tools', 'power-tools', NULL, '2024-03-15 20:55:06', '2024-03-15 20:55:06'),
  ('MDBEKOAJG5PU9XB1', 'Measuring Tools', 'measuring-tools', NULL, '2024-10-16 02:58:35', '2024-10-16 02:58:35'),
  ('MDBEKOAJVUH0WHT5', 'Hammers', 'hammers', 'MDBEKOAJSFOQKFXO', '2024-04-12 06:15:31', '2024-04-12 06:15:31'),
  ('MDBEKOAJGDRU934V', 'Screwdrivers', 'screwdrivers', 'MDBEKOAJSFOQKFXO', '2024-11-12 19:16:25', '2024-11-12 19:16:25'),
  ('MDBEKOAJEIWYPYK3', 'Wrenches', 'wrenches', 'MDBEKOAJSFOQKFXO', '2024-02-25 05:33:25', '2024-02-25 05:33:25'),
  ('MDBEKOAJFV0B3J2Y', 'Drills', 'drills', 'MDBEKOAJJE8UGA55', '2024-05-05 05:21:06', '2024-05-05 05:21:06'),
  ('MDBEKOAJV45PK52E', 'Saws', 'saws', 'MDBEKOAJJE8UGA55', '2024-03-20 22:27:29', '2024-03-20 22:27:29'),
  ('MDBEKOAJSNQXZ0FB', 'Sanders', 'sanders', 'MDBEKOAJJE8UGA55', '2024-02-19 07:36:41', '2024-02-19 07:36:41'),
  ('MDBEKOAJVTYPHWBO', 'Linear Measurement', 'linear-measurement', 'MDBEKOAJG5PU9XB1', '2024-11-10 04:25:01', '2024-11-10 04:25:01');

COMMIT;

-- ============================================================
-- Script completed successfully
-- Total records inserted: 10
-- ============================================================
