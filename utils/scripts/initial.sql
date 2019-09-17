CREATE TABLE `cabinet_offline_record` (
  `id` varchar(255) NOT NULL,
  `cabinet_id` varchar(255) NOT NULL COMMENT '柜机ID',
  `cabinet_name` varchar(255) DEFAULT NULL COMMENT '柜机名称',
  `offline_starttime` datetime DEFAULT NULL COMMENT '离线开始时间',
  `offline_endtime` datetime DEFAULT NULL COMMENT '离线结束时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
