-- ============================================================
-- SQL INSERT Script for categories table
-- ============================================================
-- Generated: 2025-07-20T07:57:20.596Z
-- Database: MYSQL
-- Records: 10
-- Generator: Mockaroo Categories Data Generator v2.0
-- ============================================================

START TRANSACTION;

INSERT INTO `categories` (`id`, `name`, `slug`, `parent_id`, `created_at`, `updated_at`)
VALUES
  ('MDBDVV3DOI45UA48', 'Hand Tools', 'hand-tools', NULL, '2024-01-17 01:33:51', '2024-01-17 01:33:51'),
  ('MDBDVV3DPCZ7JEVN', 'Power Tools', 'power-tools', NULL, '2024-03-04 02:03:43', '2024-03-04 02:03:43'),
  ('MDBDVV3DATSC4NGT', 'Measuring Tools', 'measuring-tools', NULL, '2024-01-12 03:54:04', '2024-01-12 03:54:04'),
  ('MDBDVV3DDRJ15NVC', 'Hammers', 'hammers', 'MDBDVV3DOI45UA48', '2024-07-15 18:09:20', '2024-07-15 18:09:20'),
  ('MDBDVV3D2Q3ISBJK', 'Screwdrivers', 'screwdrivers', 'MDBDVV3DOI45UA48', '2024-04-09 23:20:34', '2024-04-09 23:20:34'),
  ('MDBDVV3DUKI5QXO2', 'Wrenches', 'wrenches', 'MDBDVV3DOI45UA48', '2024-04-11 14:42:36', '2024-04-11 14:42:36'),
  ('MDBDVV3DWEVLCOEI', 'Drills', 'drills', 'MDBDVV3DPCZ7JEVN', '2024-02-28 02:51:33', '2024-02-28 02:51:33'),
  ('MDBDVV3DS7E0FEPW', 'Saws', 'saws', 'MDBDVV3DPCZ7JEVN', '2024-01-13 04:36:40', '2024-01-13 04:36:40'),
  ('MDBDVV3DA4IUQOK6', 'Sanders', 'sanders', 'MDBDVV3DPCZ7JEVN', '2024-04-11 06:50:37', '2024-04-11 06:50:37'),
  ('MDBDVV3DA8LEFVT9', 'Linear Measurement', 'linear-measurement', 'MDBDVV3DATSC4NGT', '2024-06-16 02:04:14', '2024-06-16 02:04:14');

COMMIT;

-- ============================================================
-- Script completed successfully
-- Total records inserted: 10
-- ============================================================
