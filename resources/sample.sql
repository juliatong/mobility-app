INSERT INTO `mobility_data`.`regions` (`geo_type`, `name`) VALUES
("county", "Washington County"),
("country_region", "Albania")
;

INSERT INTO `mobility_data`.`locations` (`region_id`, `sub_region`, `country`) VALUES
(1, "Indiana", "United States"),
(1, "Florida", "United States"),
(1, "Pennsylvania", "United States"),
(1, "New York", "United States"),
(1, "Oklahoma", "United States"),
(1, "Wisconsin", "United States"),
(1, "Oregon", "United States"),
(1, "Vermont", "United States"),
(1, "Nebraska", "United States"),
(1, "Tennessee", "United States"),
(1, "Maryland", "United States"),
(1, "Georgia", "United States"),
(1, "Rhode Island", "United States"),
(1, "Mississippi", "United States"),
(1, "Ohio", "United States"),
(1, "Virginia", "United States"),
(1, "Minnesota", "United States"),
(1, "Texas", "United States"),
(1, "Iowa", "United States"),
(1, "Arkansas", "United States"),
(1, "Illinois", "United States"),
(1, "Utah", "United States"),
(2, "", "")
;

INSERT INTO `mobility_data`.`direction_requests` (`location_id`, `transportation_type`, `request_date`, `requests`) VALUES
(7, "driving", "2020-01-13", 100),
(7, "driving", "2020-01-14", 99.62),
(7, "driving", "2020-01-14", 99.62),
(7, "driving", "2020-01-15", 99.42),
(7, "driving", "2020-01-16", 104.22),
(7, "driving", "2020-01-17", 119.6),
(7, "driving", "2020-01-18", 110.48),
(7, "driving", "2020-01-19", 84.75),
(7, "driving", "2020-01-20", 101.26),
(7, "driving", "2020-01-21", 103.05),
(7, "driving", "2020-01-22", 103.42),
(7, "driving", "2020-01-23", 114.71),
(7, "driving", "2020-01-24", 122.16),
(7, "driving", "2020-01-25", 113.15),
(7, "driving", "2020-01-26", 80.11),
(7, "driving", "2020-01-27", 100.62),
(7, "driving", "2020-01-28", 102.52),
(7, "driving", "2020-01-29", 106.61),
(7, "driving", "2020-01-30", 108.14),
(7, "driving", "2020-01-31", 120.17),
(7, "driving", "2020-02-01", 111.27),
(7, "driving", "2020-02-02", 73.31),
(7, "driving", "2020-02-03", 99.44),
(7, "driving", "2020-02-04", 102.21),
(7, "driving", "2020-02-05", 105.16),
(7, "driving", "2020-02-06", 109.96)
;

