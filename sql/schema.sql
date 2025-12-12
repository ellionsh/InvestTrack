-- MySQL schema for InvestTrack
CREATE DATABASE IF NOT EXISTS investtrack CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE investtrack;

CREATE TABLE IF NOT EXISTS institutions (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS products (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  institution_id BIGINT NOT NULL,
  name VARCHAR(255) NOT NULL,
  invested_amount DECIMAL(18,4) NOT NULL,
  term_months INT NOT NULL, -- 投资期限（以月计）
  purchase_date DATE,
  current_value DECIMAL(18,4),
  expected_profit DECIMAL(18,4),
  actual_profit DECIMAL(18,4),
  annualized_return DECIMAL(10,6), -- 存储年化收益率，如 0.123456 表示 12.3456%
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (institution_id) REFERENCES institutions(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
