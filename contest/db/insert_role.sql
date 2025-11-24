INSERT INTO role (team_id, needed_roles) VALUES
-- (1) 현재 PM·FE·BE는 있지만, 데이터 중심 팀 → 데이터 분석가 / DevOps도 필요해 보임
(1, 'Backend_Developer'),
(1, 'Analyst'),
(1, 'DevOps'),

-- (2) 기획·디자인·FE는 있지만 백엔드 없음 → 백엔드 + 데이터분석가 필요
(2, 'Backend_Developer'),
(2, 'Analyst'),

-- (3) 백엔드·분석만 있음 → 프론트엔드 + 디자이너 필요
(3, 'Frontend_Developer'),
(3, 'Web_Designer'),

-- (4) PM·BE·분석 있음 → 프론트엔드 + 디자이너 필요
(4, 'Frontend_Developer'),
(4, 'Designer'),

-- (5) FE·디자이너 있음 → 백엔드 + 기획자 필요
(5, 'Backend_Developer'),
(5, 'Manager'),

-- (6) 분석·FE 있음 → 백엔드 + DevOps 필요
(6, 'Backend_Developer'),
(6, 'DevOps'),

-- (7) 기획·BE·FE 있음 → 데이터 분석가 필요 (모델 연동)
(7, 'Analyst'),

-- (8) PM·디자이너·FE 있음 → 데이터 분석가 필요
(8, 'Analyst'),

-- (9) 데이터 사이언티스트·BE 있음 → 프론트엔드 + 디자이너 필요
(9, 'Frontend_Developer'),
(9, 'Designer'),

-- (10) 기획·BE·디자이너 있음 → 프론트엔드 + Analyst 필요
(10, 'Frontend_Developer'),
(10, 'Analyst');



INSERT INTO role (team_id, needed_roles) VALUES
(11, 'Frontend_Developer'),
(12, 'Frontend_Developer'),
(13, 'Frontend_Developer'),
(14, 'Manager'),
(15, 'Analyst'),
(16, 'Frontend_Developer'),
(17, 'Backend_Developer'),
(18, 'Designer'),
(19, 'Designer'),
(20, 'Frontend_Developer');

INSERT INTO role (team_id, needed_roles) VALUES
-- (21) 데이터 분석 중심 팀 → 프론트엔드 시각화 + 디자이너 협업 가능성
(21, 'Frontend_Developer'),
(21, 'Designer'),

-- (22) PM + 데이터 엔지니어 팀 → 모델 서빙용 백엔드 + DevOps 필요
(22, 'Backend_Developer'),
(22, 'DevOps'),

-- (23) 데이터 분석가 + FE → 데이터 처리 및 연결용 백엔드 필요
(23, 'Backend_Developer'),

-- (24) PM + BE + 분석가 → 프론트엔드 + 디자이너 (대시보드 제작)
(24, 'Frontend_Developer'),
(24, 'Designer'),

-- (25) 데이터 사이언티스트 + FE → 백엔드 + DevOps (AI 시각화)
(25, 'Backend_Developer'),
(25, 'DevOps'),

-- (26) 기획 + 데이터 엔지니어 → 프론트엔드 + 디자이너 필요
(26, 'Frontend_Developer'),
(26, 'Designer'),

-- (27) 데이터 분석 + BE → 데이터 자동화 관련 DevOps 또는 Analyst 강화
(27, 'Backend_Developer'),
(27, 'Analyst'),

-- (28) PM + 데이터 사이언티스트 + 디자이너 → 대시보드용 프론트엔드 필요
(28, 'Frontend_Developer'),

-- (29) 데이터 엔지니어 + BE → 분석 중심 팀으로 Analyst 보강
(29, 'Analyst'),

-- (30) 기획 + 분석 + FE → 서비스 디자인 보완
(30, 'Designer');

INSERT INTO role (team_id, needed_roles) VALUES
-- (31) 기획·디자인만 있음 → 구현 담당 개발자 필요 (프론트엔드 중심)
(31, 'Frontend_Developer'),

-- (32) PM·기획·디자인 있음 → 프로토타입 개발할 FE + 서버 연결할 BE 필요
(32, 'Frontend_Developer'),
(32, 'Backend_Developer'),

-- (33) 기획·FE 있음 → 서비스 완성 위해 백엔드 필요
(33, 'Backend_Developer'),

-- (34) 디자인·마케팅 중심 → 팀 리딩할 PM 필요
(34, 'Manager'),

-- (35) 기획·디자인·PM 있음 → 발표자나 마케팅 중심 역할 추가
(35, 'Marketer'),

-- (36) 기획·디자인·FE 있음 → 리서치 강화 위해 기획자 추가
(36, 'Manager'),
(36, 'Surveyor'),

-- (37) 기획·마케팅·디자인 있음 → 시각화 작업 보조 디자이너 필요
(37, 'Designer'),

-- (38) PM·디자이너 있음 → 브랜딩/로고 중심 → 디자이너 추가
(38, 'Designer'),

-- (39) 기획·개발 있음 → 시각화 담당 디자이너 필요
(39, 'Designer'),

-- (40) 기획·디자인·BE 있음 → 홍보 및 브랜딩 담당 마케터 필요
(40, 'Marketer');

INSERT INTO role (team_id, needed_roles) VALUES
-- (41) 건축 설계 중심 → 3D 모델링 보조 디자이너 필요
(41, 'Designer'),

-- (42) PM + 건축학도 → 시뮬레이션 구현할 개발자 (FE + BE)
(42, 'Frontend_Developer'),
(42, 'Backend_Developer'),

-- (43) 도시계획 + 디자인 → UX 기획 PM 필요
(43, 'Manager'),

-- (44) 기획 + 엔지니어 → 데이터 기반 도시 시스템 → 백엔드 + Analyst
(44, 'Backend_Developer'),
(44, 'Analyst'),

-- (45) 건축 + 디자인 + BE → 시각화 담당 프론트엔드
(45, 'Frontend_Developer'),

-- (46) PM + 디자이너 + 분석가 → 데이터 사이언티스트 추가
(46, 'Analyst'),

-- (47) 도시계획 + 엔지니어 + 디자이너 → 에너지 계산 담당 BE
(47, 'Backend_Developer'),

-- (48) 건축 + 기획 + 디자인 → 시각디자이너 추가
(48, 'Designer'),

-- (49) 디자인 + 엔지니어 → 도시 데이터 시각화 → Analyst 추가
(49, 'Analyst'),

-- (50) PM + 건축학도 + FE → BE 추가
(50, 'Backend_Developer');

INSERT INTO role (team_id, needed_roles) VALUES
-- (51) 기획 + 마케팅 + 디자인 → 서비스 구현용 백엔드 필요
(51, 'Backend_Developer'),

-- (52) PM + 기획 → 서비스 브랜딩 담당 디자이너 필요
(52, 'Designer'),

-- (53) 기획 + 개발 → 프로토타입 완성을 위한 디자이너
(53, 'Designer'),

-- (54) PM + 디자이너 + 마케터 → 전략 구체화할 기획자 추가
(54, 'Manager'),

-- (55) 기획 + 디자이너 + 개발 → MVP 완성용 프론트엔드 강화
(55, 'Frontend_Developer'),

-- (56) PM + 기획 + 개발 → 마케팅 전략 담당 마케터 필요
(56, 'Marketer'),

-- (57) 기획 + 디자이너 → 런칭 준비용 개발자 (FE 중심)
(57, 'Frontend_Developer'),

-- (58) 디자인 + 마케팅 + 개발 → 비즈니스 분석 기획자 필요
(58, 'Manager'),

-- (59) 기획 + FE + BE → 서비스 개선 위한 디자이너 필요
(59, 'Designer'),

-- (60) PM + 기획 + 디자인 + 개발 → 제품 고도화용 프론트엔드 추가
(60, 'Frontend_Developer');

INSERT INTO role (team_id, needed_roles) VALUES
-- (61) PM·BE·FE 있음 → AI 센서 데이터 분석용 데이터 엔지니어 추가
(61, 'Analyst'),

-- (62) 기획·BE·디자인 팀 → UI 개발 담당 프론트엔드 필요
(62, 'Frontend_Developer'),

-- (63) 데이터 엔지니어 중심 → 시각화 담당 프론트엔드 보강
(63, 'Frontend_Developer'),
(63, 'Designer'),

-- (64) PM·기획·BE → API 연동용 프론트엔드 필요
(64, 'Frontend_Developer'),

-- (65) 기획·디자인·BE → 앱 UI 구현 FE 필요
(65, 'Frontend_Developer'),

-- (66) 분석·엔지니어 팀 → 데이터 수집/학습 담당 백엔드 필요
(66, 'Backend_Developer'),

-- (67) PM·디자인·FE → 데이터 연결용 백엔드 필요
(67, 'Backend_Developer'),

-- (68) 기획·BE·마케팅 → 홍보 시각화 디자이너 필요
(68, 'Designer'),

-- (69) BE·데이터 엔지니어 → 시각화 담당 프론트엔드 필요
(69, 'Frontend_Developer'),

-- (70) PM·FE·분석 → 기획자 보강 필요
(70, 'Manager');

INSERT INTO role (team_id, needed_roles) VALUES
(71, 'Frontend_Developer'),
(72, 'Designer'),
(73, 'Marketer'),
(74, 'Manager'),
(75, 'Designer'),
(76, 'Manager'),
(76, 'Surveyor'),
(77, 'Backend_Developer'),
(78, 'Frontend_Developer'),
(79, 'Backend_Developer'),
(80, 'Frontend_Developer');

INSERT INTO role (team_id, needed_roles) VALUES
-- (81) 기획 + 연구 중심 → 자료 조사·통계 분석 담당 분석가
(81, 'Analyst'),
(81, 'Surveyor'),

-- (82) 화학연구 + 데이터 분석 → 시각화 담당 디자이너
(82, 'Designer'),

-- (83) 기획 + 디자인 + 연구 → 발표 자료 제작 및 정리 담당 기획자
(83, 'Manager'),

-- (84) 연구 + 분석 + 디자인 → 생활 데이터 분석용 백엔드 필요
(84, 'Backend_Developer'),

-- (85) 기획 + 연구 + 마케팅 → 검증용 데이터 분석가
(85, 'Analyst'),

-- (86) 연구 중심 + 디자인 → 시각화 강화용 디자이너 추가
(86, 'Designer'),

-- (87) 기획 + 연구 + 분석 → 시각화 개발 담당 프론트엔드
(87, 'Frontend_Developer'),

-- (88) 연구 + 디자인 → 리포트 정리 담당 기획자
(88, 'Manager'),

-- (89) 기획 + 연구 → 데이터 분석가 추가
(89, 'Analyst'),

-- (90) 연구 + 기획 + 디자인 → 과학 커뮤니케이션 담당 디자이너
(90, 'Designer');

INSERT INTO role (team_id, needed_roles) VALUES
-- (91) 기획 중심 팀 → 데이터 분석 기반 사회문제 연구
(91, 'Analyst'),

-- (92) PM + 디자인 → 캠페인 콘텐츠 제작용 마케터
(92, 'Marketer'),

-- (93) 데이터 + 디자인 → 정책 시각화 담당 프론트엔드
(93, 'Frontend_Developer'),

-- (94) 기획 + 디자인 → 현장 인터뷰 담당 조사자
(94, 'Surveyor'),

-- (95) PM + 디자인 + 마케팅 → 브랜드 전략 담당 기획자
(95, 'Manager'),

-- (96) 기획 + 디자인 → 사회문제 데이터 분석 담당 백엔드
(96, 'Backend_Developer'),

-- (97) 디자인 + 기획 → 시민참여 플랫폼 화면 담당 프론트엔드
(97, 'Frontend_Developer'),

-- (98) 기획 + 분석 + 마케팅 → 소셜 임팩트 지표 설계 담당 연구자
(98, 'Surveyor'),

-- (99) 디자인 + 백엔드 → 시민참여 앱 프론트엔드
(99, 'Frontend_Developer'),

-- (100) PM + 기획 + 디자인 + 연구 → 정책 제안서용 연구원 추가
(100, 'Surveyor');

INSERT INTO role (team_id, needed_roles) VALUES
-- (101) PM·BE·Analyst → 모델 API 배포를 맡을 백엔드 강화
(101, 'Backend_Developer'),
(101, 'DevOps'),

-- (102) 기획·디자인·FE → LLM UX/UI 설계 디자이너 보강
(102, 'Designer'),

-- (103) 데이터 엔지니어 + 백엔드 → 데이터 수집 및 전처리 담당 분석가
(103, 'Analyst'),

-- (104) PM·분석·디자인 → AI 시각화 담당 프론트엔드 필요
(104, 'Frontend_Developer'),

-- (105) 기획·BE·FE → AI 연동 및 파이프라인 구축용 데이터 엔지니어
(105, 'Analyst'),

-- (106) 분석 + BE 중심 → 데이터셋 구축 담당 Surveyor(데이터 어노테이터 개념)
(106, 'Surveyor'),

-- (107) PM·기획·FE → 피드백 시스템 백엔드 필요
(107, 'Backend_Developer'),

-- (108) 기획·디자인 → 인터랙션 중심 프론트엔드 필요
(108, 'Frontend_Developer'),

-- (109) 데이터 사이언티스트 + 엔지니어 + 디자이너 → 시각화 전문가
(109, 'Analyst'),
(109, 'Designer'),

-- (110) PM·기획·BE·디자이너 → AI-IoT 통합 프로젝트용 엔지니어
(110, 'DevOps');

INSERT INTO role (team_id, needed_roles) VALUES
-- (111) 기획 + 디자인 팀 → 영상 콘텐츠 담당 영상 디자이너
(111, 'Designer'),

-- (112) PM + 디자인 + 카피 → 콘셉트 시각화 담당 그래픽 디자이너
(112, 'Designer'),

-- (113) 디자인 + 마케팅 → SNS 운영 전략 기획자 필요
(113, 'Manager'),

-- (114) 기획 + 디자인 + 영상편집 → 촬영 담당 보조 (Surveyor 성격)
(114, 'Surveyor'),

-- (115) PM + 마케팅 + 디자인 → 스토리 캠페인용 카피라이터
(115, 'Marketer'),

-- (116) 기획 + 디자인 → 브랜드 로고 제작 디자이너
(116, 'Designer'),

-- (117) 디자인 + 마케팅 → 브랜드 기획서 작성 담당 기획자
(117, 'Manager'),

-- (118) 기획 + 디자인 + 작가 → 일러스트 제작 디자이너
(118, 'Designer'),

-- (119) PM + 디자인 → 패키지 시각화 담당 디자이너
(119, 'Designer'),

-- (120) 기획 + 카피 + 디자인 → 브랜드 메시지 시각화 디자이너
(120, 'Designer');

INSERT INTO role (team_id, needed_roles) VALUES
(121, 'Analyst'),
(122, 'Surveyor'),
(123, 'Backend_Developer'),
(123, 'DevOps'),
(124, 'Designer'),
(125, 'Designer'),
(126, 'Frontend_Developer'),
(127, 'Designer'),
(128, 'Analyst'),
(129, 'Designer'),
(130, 'Analyst');

INSERT INTO role (team_id, needed_roles) VALUES
(131, 'Designer'),
(132, 'Manager'),
(133, 'Frontend_Developer'),
(134, 'Designer'),
(135, 'Manager'),
(136, 'Backend_Developer'),
(137, 'Designer'),
(138, 'Frontend_Developer'),
(139, 'Marketer'),
(140, 'Marketer');

INSERT INTO role (team_id, needed_roles) VALUES
(141, 'Designer'),
(142, 'Analyst'),
(143, 'Surveyor'),
(144, 'Designer'),
(145, 'Analyst'),
(146, 'Designer'),
(147, 'Analyst'),
(148, 'Designer'),
(149, 'Designer'),
(150, 'Manager');

INSERT INTO role (team_id, needed_roles) VALUES
(151, 'Analyst'),
(152, 'Designer'),
(153, 'Surveyor'),
(154, 'Frontend_Developer'),
(155, 'Analyst'),
(156, 'Marketer'),
(157, 'Manager'),
(158, 'Designer'),
(159, 'Marketer'),
(160, 'Designer');

INSERT INTO role (team_id, needed_roles) VALUES
(161, 'Backend_Developer'),
(162, 'Backend_Developer'),
(163, 'Designer'),
(164, 'DevOps'),
(165, 'Backend_Developer'),
(166, 'DevOps'),
(167, 'Designer'),
(168, 'Frontend_Developer'),
(169, 'Analyst'),
(170, 'Backend_Developer');

INSERT INTO role (team_id, needed_roles) VALUES
(171, 'Marketer'),
(172, 'Designer'),
(173, 'Frontend_Developer'),
(174, 'Marketer'),
(175, 'Frontend_Developer'),
(176, 'Marketer'),
(177, 'Designer'),
(178, 'Manager'),
(179, 'Backend_Developer'),
(180, 'Designer');

INSERT INTO role (team_id, needed_roles) VALUES
(181, 'Surveyor'),
(182, 'Backend_Developer'),
(183, 'Backend_Developer'),
(184, 'Analyst'),
(185, 'Designer'),
(186, 'Analyst'),
(187, 'Surveyor'),
(188, 'Marketer'),
(189, 'Analyst'),
(190, 'Manager');


INSERT INTO role (team_id, needed_roles) VALUES
(191, 'Designer'),
(192, 'Backend_Developer'),
(193, 'Designer'),
(194, 'Marketer'),
(195, 'Designer'),
(196, 'Backend_Developer'),
(197, 'Designer'),
(198, 'Marketer'),
(199, 'Frontend_Developer'),
(200, 'Marketer');