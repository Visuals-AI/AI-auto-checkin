CREATE TABLE IF NOT EXISTS `t_face_feature` (
  `i_id`                    INTEGER PRIMARY KEY AUTOINCREMENT,
  `s_image_id`              TEXT(64),
  `s_name`                  TEXT(128),
  `f_feature`               TEXT,
  `s_original_image_path`   TEXT(512),
  `s_feature_image_path`    TEXT(512)
);
