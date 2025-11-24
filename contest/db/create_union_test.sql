-- 데이터베이스 만들기 (없으면 생성)
DROP DATABASE IF EXISTS union_test;

CREATE DATABASE IF NOT EXISTS `union_test`
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_general_ci;

-- 이 데이터베이스 사용
USE `union_test`;

CREATE TABLE users (
  users_id integer PRIMARY KEY AUTO_INCREMENT,
  login_id varchar(10),
  password varchar(255),
  username varchar(40) NOT NULL,
  email varchar(255) UNIQUE NOT NULL,
  created_at  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE contests (
  contest_id integer PRIMARY KEY AUTO_INCREMENT,
  contest_name varchar(200) NOT NULL,
  summary text,
  field ENUM ('AI', 'ART', 'DATA', 'IDEA', 'ARCHITECTURE', 'BUSINESS', 'IT', 'STARTUP', 'SCIENCE', 'SOCIAL'),
  reception_start_date date,
  reception_end_date date,
  start_date  date,
  end_date date,
  activity_type ENUM ('OFFLINE', 'ONLINE', 'HYBRID'),
  cost integer,
  reward integer,
  eligibility varchar(255)
);

CREATE TABLE team_info (
  team_id integer PRIMARY KEY AUTO_INCREMENT,
  current_team varchar(200),
  recruit_date date,
  collab_tool text,
  contact_type ENUM ('KAKAO', 'EMAIL', 'DM', 'PHONE', 'OTHER'),
  contact_value text,
  extra_note text,
  seeking_text text,
  culture_text text
);

CREATE TABLE team_post (
  post_id integer PRIMARY KEY AUTO_INCREMENT,
  team_id integer NOT NULL,
  leader_id integer NOT NULL,
  contest_id integer,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  
  CONSTRAINT fk_team_post_team
    FOREIGN KEY (team_id) REFERENCES team_info(team_id)
    ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_team_post_leader
    FOREIGN KEY (leader_id) REFERENCES users(users_id)
    ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT fk_team_post_contest
    FOREIGN KEY (contest_id) REFERENCES contests(contest_id)
    ON DELETE SET NULL ON UPDATE CASCADE
);



CREATE TABLE role (
  role_id INT PRIMARY KEY AUTO_INCREMENT,
  team_id integer NOT NULL,
  needed_roles ENUM ('Manager', 'Backend_Developer', 'Frontend_Developer', 'Web_Designer', 'Designer', 'Analyst', 'DevOps', 'Surveyor', 'Marketer') NOT NULL,
  CONSTRAINT fk_roles_team
    FOREIGN KEY (team_id) REFERENCES team_info(team_id)
    ON DELETE CASCADE ON UPDATE CASCADE,
   UNIQUE KEY uq_team_role (team_id, needed_roles)
);

-- contests
CREATE INDEX idx_contests_field       ON contests(field);
CREATE INDEX idx_contests_activity    ON contests(activity_type);
CREATE INDEX idx_contests_reception   ON contests(reception_start_date, reception_end_date);
CREATE INDEX idx_contests_period      ON contests(start_date, end_date);
CREATE FULLTEXT INDEX ft_contests_text ON contests (contest_name, summary, eligibility);

-- role
CREATE INDEX idx_role_team_needed ON role(team_id, needed_roles);

-- team_post
CREATE INDEX idx_team_post_contest ON team_post(contest_id);
CREATE INDEX idx_team_post_team    ON team_post(team_id);

-- team_info (옵션: 연락수단/마감 조회)
CREATE INDEX idx_team_info_contact ON team_info(contact_type);
CREATE INDEX idx_team_info_recruit ON team_info(recruit_date);