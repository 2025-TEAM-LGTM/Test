DROP DATABASE IF EXISTS union_final;


CREATE DATABASE union_final
    DEFAULT CHARACTER SET utf8mb4
    DEFAULT COLLATE utf8mb4_general_ci;

USE union_final;


CREATE TABLE `user` (
  `user_id` BIGINT AUTO_INCREMENT PRIMARY KEY NOT NULL,
  `login_id` char(50) NOT NULL,
  `password` char(50) NOT NULL,
  `username` char(50) NOT NULL,
  `email` char(50) NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL
);

CREATE TABLE `contest` (
  `contest_id` BIGINT AUTO_INCREMENT PRIMARY KEY NOT NULL,
  `contest_name` varchar(255),
  `summary` text,
  `field` ENUM ('AI', 'ART', 'DATA', 'IDEA', 'ARCHITECTURE', 'BUSINESS', 'IT', 'STARTUP', 'SCIENCE', 'SOCIAL'),
  `reception_sdate` datetime,
  `reception_edate` datetime,
  `activity_sdate` datetime,
  `activity_edate` datetime,
  `activity_type` ENUM ('OFFLINE', 'ONLINE', 'HYBRID'),
  `reward` int,
  `eligibility` text
);

CREATE TABLE `team_info` (
  `team_id` BIGINT AUTO_INCREMENT PRIMARY KEY NOT NULL,
  `current_team` int,
  `recruit_edate` date,
  `collab_tool` text,
  `contact_email` text,
  `contact_etc` text,
  `seeking_text` text,
  `culture_text` text,
  `extra_text` text
);

CREATE TABLE `team_post` (
  `post_id` BIGINT AUTO_INCREMENT PRIMARY KEY NOT NULL,
  `team_id` BIGINT NOT NULL,
  `leader_id` BIGINT NOT NULL,
  `contest_id` BIGINT NOT NULL,
  `title` text,
  `summary` text,
  `created_at` datetime,
  `updated_at` datetime
);


CREATE TABLE `role` (
  `role_id` BIGINT AUTO_INCREMENT PRIMARY KEY NOT NULL,
  `team_id` BIGINT NOT NULL,
  `needed_role` ENUM ('Manager', 'Backend_Developer', 'Frontend_Developer', 'Web_Designer', 'Designer', 'Analyst', 'DevOps', 'Surveyor', 'Marketer'),
  `headcount` int
);

CREATE TABLE `portfolio_post` (
  `portfolio_post_id` BIGINT AUTO_INCREMENT PRIMARY KEY NOT NULL,
  `user_id` BIGINT NOT NULL,
  `created_at` datetime,
  `updated_at` datetime
);

CREATE TABLE `user_profile` (
  `profile_id` BIGINT AUTO_INCREMENT PRIMARY KEY NOT NULL,
  `user_id` BIGINT NOT NULL,
  `portfolio_post_id` BIGINT NOT NULL,
  `university` ENUM ('EWHA', 'OTHER'),
  `major` varchar(255),
  `dual_major` varchar(255),
  `entrance_year` int,
  `birth_year` int,
  `status` ENUM ('ENROLLED', 'LEAVE', 'DEFERRED', 'GRADUATED', 'TRANSFER', 'EXCHANGE', 'OTHER'),
  `gender` ENUM('FEMALE', 'MALE', 'NONBINARY')
);

CREATE TABLE `portfolio_project` (
  `portfolio_project_id` BIGINT AUTO_INCREMENT PRIMARY KEY NOT NULL,
  `portfolio_post_id` BIGINT NOT NULL,
  `project_title` varchar(200),
  `project_headcount` int,
  `project_period` int,
  `project_domain` varchar(200),
  `s_text` longtext,
  `t_text` longtext,
  `r_text` longtext,
  `a_text` longtext,
  `created_at` datetime,
  `updated_at` datetime
);

CREATE TABLE `portfolio_keyword` (
  `portfolio_keyword_id` BIGINT AUTO_INCREMENT PRIMARY KEY NOT NULL,
  `portfolio_project_id` BIGINT NOT NULL,
  `keyword` json
);

ALTER TABLE `team_post`
  ADD CONSTRAINT fk_team_post_leader
    FOREIGN KEY (`leader_id`) REFERENCES `user`(`user_id`);

ALTER TABLE `portfolio_post`
  ADD CONSTRAINT fk_portfolio_post_user
    FOREIGN KEY (`user_id`) REFERENCES `user`(`user_id`);

ALTER TABLE `user_profile`
  ADD CONSTRAINT fk_user_profile_user
    FOREIGN KEY (`user_id`) REFERENCES `user`(`user_id`);

ALTER TABLE `team_post`
  ADD CONSTRAINT fk_team_post_team_info
    FOREIGN KEY (`team_id`) REFERENCES `team_info`(`team_id`);

ALTER TABLE `role` 
	ADD CONSTRAINT fk_role_team_info
	  FOREIGN KEY (`team_id`) REFERENCES `team_info` (`team_id`);

ALTER TABLE `team_post` 
	ADD CONSTRAINT fk_team_post_contest
	  FOREIGN KEY (`contest_id`) REFERENCES `contest` (`contest_id`);
    
ALTER TABLE `user_profile`
  ADD CONSTRAINT fk_user_profile_portfolio_post
    FOREIGN KEY (`portfolio_post_id`) REFERENCES `portfolio_post`(`portfolio_post_id`);

ALTER TABLE `portfolio_project` 
	ADD CONSTRAINT fk_portfolio_project_portfolio_post
	  FOREIGN KEY (`portfolio_post_id`) REFERENCES `portfolio_post` (`portfolio_post_id`);

ALTER TABLE `portfolio_keyword`
  ADD CONSTRAINT fk_portfolio_keyword_project
    FOREIGN KEY (`portfolio_project_id`) REFERENCES `portfolio_project`(`portfolio_project_id`);

ALTER TABLE `portfolio_keyword`
	ADD CONSTRAINT chk_keyword_domain_enum
		CHECK (
		  JSON_UNQUOTE(JSON_EXTRACT(`keyword`, '$.S.domain')) IN (
			'EDUCATION',
			'LIFESTYLE',
			'SOCIAL',
			'ENTERTAINMENT',
			'HEALTHCARE',
			'PRODUCTIVITY',
			'E_COMMERCE',
			'TRAVEL',
			'FINTECH'
		  )
	);
ALTER TABLE `portfolio_keyword`
	ADD CONSTRAINT chk_keyword_role_enum
		CHECK (
		  JSON_UNQUOTE(JSON_EXTRACT(`keyword`, '$.T.role')) IN (
			'BACKEND_DEVELOPER',
			'FRONTEND_DEVELOPER',
			'UX/UI_DESIGNER',
			'PM',
			'AI_DEVELOPER'
		  )
);