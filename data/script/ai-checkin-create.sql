CREATE TABLE IF NOT EXISTS `t_face_feature` (
  `i_id`                    INTEGER PRIMARY KEY AUTOINCREMENT,
  `s_image_id`              TEXT(64),
  `s_name`                  TEXT(128),
  `f_feature`               TEXT,
  `s_align_size`            TEXT(32),
  `s_mesh_image_path`       TEXT(512),
  `s_detection_image_path`  TEXT(512),
  `s_alignment_image_path`  TEXT(512)
);


CREATE TABLE IF NOT EXISTS `t_checkin` (
  `i_id`                    INTEGER PRIMARY KEY AUTOINCREMENT,
  `s_date`                  TEXT(16),
  `i_checkin_hour`          INTEGER,
  `i_checkin_minute`        INTEGER,
  `i_checkout_hour`         INTEGER,
  `i_checkout_minute`       INTEGER,
  `i_work_time`             INTEGER
);
