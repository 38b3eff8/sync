CREATE TABLE file_md5 (
  name       TEXT,
  md5        TEXT,
  created_at TIMESTAMP DEFAULT (datetime('now', 'localtime')),
  updated_at TIMESTAMP DEFAULT (datetime('now', 'localtime'))
);