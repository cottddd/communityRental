# comumnityRental
2024-2 DB Project

## 1. 프로젝트 개요 (Project topic)
> 사용한 언어 및 라이브러리
### 1. 프로그래밍 언어: Python
* 프로젝트 전반에서 비즈니스 로직을 구현.  
* 사용자 입력 처리, 데이터베이스 연동, 프로그램의 주요 기능 개발에 사용.
### 2. 사용된 라이브러리 및 모듈:
* pymysql:  
  * Python과 MySQL 데이터베이스 간의 연결 및 쿼리 실행을 지원.  
* bcrypt:  
  * 사용자 비밀번호의 안전한 해싱과 검증을 위해 사용.  
* getpass:  
  * 비밀번호 입력 시 화면에 표시되지 않도록 처리.  
* datetime:  
  * 대여 날짜 및 시간 관련 기능 구현.  
* sys:  
  * 프로그램 종료 또는 예외 처리와 같은 기본적인 시스템 작업 관리.  
### 3. 데이터베이스:
* MySQL:  
  * 데이터 저장 및 관리에 사용.  
  * Community Rental 플랫폼의 사용자, 장비, 대여 기록 및 리뷰 데이터 관리.
<br/> </br>
> 프로젝트 개요
### 지역 기반 장비 대여 서비스 플랫폼 데이터베이스
이 프로젝트의 주제는 사용자가 지역 기반으로 장비를 등록하거나 대여할 수 있는 플랫폼을 지원하는 데이터베이스 시스템을 설계하고 구현하는 것입니다.  
이 시스템은 장비 등록 및 대여 관리, 리뷰 및 평점 관리, 지역 기반 필터링, 사용자 및 관리자 관리 등의 주요 기능을 제공합니다.  

**구현 기능**
* **사용자 관리:** 사용자 회원가입, 로그인, 지역 설정, 리뷰 작성, 장비 대여 이력 조회 등의 기능을 제공합니다.
* **장비 관리:** 장비 등록, 수정, 삭제, 대여 가능 날짜 설정 등의 기능을 제공합니다.
* **대여 관리:** 대여 요청, 승인/거절, 대여 상태 변경, 대여 이력 조회 등의 기능을 제공합니다.
* **리뷰 관리:** 사용자와 장비에 대한 리뷰를 작성하고 확인할 수 있는 기능을 제공합니다.
* **관리자 관리:** 관리자는 모든 데이터를 관리하고, 사용자 계정을 추가하거나 제거할 수 있습니다.
<br/> </br>
## 2.	사용자 (역할) (Users / Roles)
### 1. Borrower (대여자):
* 장비를 검색하고 대여 요청을 보냅니다.
* 대여 완료 후 장비와 대여자(Lender)에 대한 리뷰를 작성할 수 있습니다.
* 자신의 대여 이력을 조회할 수 있습니다.
### 2. Lender (장비 등록자):
* 장비를 등록하고, 대여 가능한 날짜와 상태를 관리합니다.
* Borrower의 대여 요청을 승인하거나 거절할 수 있습니다.
* Borrower에 대한 리뷰를 작성할 수 있습니다.
### 3. Admin (관리자):
* 모든 사용자와 장비 데이터를 관리합니다.
* Admin 계정을 생성하여 시스템을 관리할 권한을 가집니다.  
<br/> </br>
## 3.	기능 (Functions)
### 1. 사용자 등록 및 로그인
* **사용자:** 모든 사용자 (Lender, Borrower, Admin)
* **설명:** 사용자 등록 시 이름, 연락처, 비밀번호, 지역을 입력받아 데이터베이스에 저장하며, 비밀번호는 해싱 처리. 로그인 시 이름과 비밀번호를 검증하여 사용자의 유효성을 확인.
* **사용된 SQL 기능:**
  * **INSERT:** 신규 사용자를 User 테이블에 추가.
  * **SELECT:** 로그인 시 입력된 정보와 테이블 데이터를 비교.
  * **CONSTRAINT:** 지역 정보와 비밀번호 형식을 검증.

### 2. 장비 등록
* **사용자:** Lender
* **설명:** Lender는 장비를 등록할 수 있으며, 등록 시 카테고리, 이름, 품질, 대여 가격, 대여 불가능 날짜를 입력.
* **사용된 SQL 기능:**
  * **INSERT:** 신규 장비를 Equipment 테이블에 추가.
  * **FOREIGN KEY:** 등록한 Lender의 ID와 지역 정보를 참조.
  * **GROUP_CONCAT:** 대여 불가능 날짜를 정렬하여 조회.

### 3. 장비 검색 및 대여 요청
* **사용자:** Borrower
* **설명:** Borrower는 카테고리 또는 이름 기반으로 장비를 검색하고, 같은 지역의 장비만 조회 가능. 검색한 장비에 대해 대여 요청 메시지를 보낼 수 있음.
* **사용된 SQL 기능:**
  * **SELECT:** WHERE 절을 사용하여 Borrower와 동일한 지역의 장비 필터링.
  * **LIKE:** 이름 검색 시 부분 일치를 지원.
  * **INSERT:** 대여 요청 메시지를 Message 테이블에 추가.
  * **JOIN:** Lender 및 장비 정보를 통합하여 조회.

### 4. 장비 상태 관리
* **사용자:** Lender
* **설명:** Lender는 장비의 상태를 "대여 가능", "예약 중", "대여 중"으로 변경 가능하며, 대여 불가능 날짜를 추가/삭제할 수 있음.
* **사용된 SQL 기능:**
  * **UPDATE:** 장비 상태를 Equipment 테이블에서 변경.
  * **DELETE:** 특정 대여 불가능 날짜를 UnavailableDates 테이블에서 삭제.
  * **INSERT:** 신규 대여 불가능 날짜를 추가.

### 5. 거래 관리
* **사용자:** Borrower 및 Lender
* **설명:** 거래 요청 및 상태 변경을 통해 "예약 중" → "대여 중" → "반납 완료"로 진행되며, 각 거래는 기록으로 남음.
* **사용된 SQL 기능:**
  * **INSERT:** 신규 거래를 RentalTransaction 테이블에 기록.
  * **UPDATE:** 거래 상태를 업데이트.
  * **CONSTRAINT:** 거래의 유효성을 보장 (Lender와 Borrower가 동일 지역 내에 있는지 확인).

### 6. 메시지 기능
* **사용자:** 모든 사용자 (Lender, Borrower)
* **설명:** Lender와 Borrower 간 메시지를 주고받을 수 있으며, 메시지 기록이 저장됨.
* **사용된 SQL 기능:**
  * **INSERT:** 메시지를 Message 테이블에 추가.
  * **SELECT:** 사용자 간 대화 내용을 검색 및 정렬.
  * **GROUP BY:** 대화 목록을 마지막 메시지 기준으로 그룹화.

### 7. 리뷰 기능
#### (1) 장비 리뷰
* **사용자:** Borrower
* **설명:** 장비를 대여한 Borrower가 품질 점수(최상~하)와 코멘트를 입력하여 리뷰를 작성. 작성된 리뷰는 평균 품질 점수로 업데이트됨.
* **사용된 SQL 기능:**
  * **INSERT:** 리뷰를 RentalTransaction 테이블에 추가.
  * **UPDATE:** 품질 점수를 Equipment 테이블에 업데이트.
  * **AVG:** 모든 리뷰의 평균 품질 점수를 계산.
#### (2) 사용자 리뷰
* **사용자:** Lender 및 Borrower
* **설명:** 거래 완료 후 Borrower와 Lender가 서로에 대한 평점과 리뷰를 남길 수 있음.
* **사용된 SQL 기능:**
  * **INSERT:** 리뷰를 RentalTransaction 테이블에 추가.
  * **SELECT:** 기존 리뷰를 조회.
  * **ORDER BY:** 최신 리뷰를 기준으로 정렬.

### 8. 관리자 기능 (Admin)
* **사용자:** Admin
* **설명:** 관리자는 사용자 계정 및 장비 등록 내역을 조회하거나 삭제할 수 있음.
* **사용된 SQL 기능:**
  * **DELETE:** 비활성화된 사용자나 장비 데이터를 삭제.
  * **SELECT:** 모든 데이터 조회.
  * **JOIN:** 사용자와 장비 데이터를 통합하여 상태 확인.
<br/> </br>
## 4.	데이터베이스 스키마 및 다이어그램 (Database schema / Schema diagram)
### 1. user 테이블
* 기능
  * 사용자의 정보를 관리하기 위한 테이블로, 사용자는 플랫폼에 가입 및 로그인을 통해 자신의 정보를 제공.
  * 사용자의 지역, 평점, 리뷰 수 등의 정보를 기반으로 지역 기반 서비스 제공.
* 컬럼
  * ID (int, Primary Key, AUTO_INCREMENT): 사용자 고유 ID.
  * name (varchar(50)): 사용자 이름.
  * contact (varchar(100)): 사용자 연락처.
  * rating (float, Default 0): 사용자 평점.
  * review_count (int, Default 0): 사용자에게 작성된 리뷰의 개수.
  * password (varchar(255)): 해싱된 비밀번호.
  * region (varchar(50)): 사용자가 선택한 지역.
  * is_admin (tinyint(1), Default 0): 사용자가 관리자인지 여부.
* 제약 조건
  * ID: Primary Key.
  * region: Default 값은 서울.
  * password: Null 불허.

### 2. equipment 테이블
* 기능
  * 등록된 장비 정보를 관리하기 위한 테이블로, Lender가 등록한 장비의 이름, 카테고리, 품질, 대여 가능 여부 등을 저장.
* 컬럼
  * equip_ID (int, Primary Key, AUTO_INCREMENT): 장비 고유 ID.
  * name (varchar(100)): 장비 이름.
  * category (varchar(50)): 장비 카테고리.
  * lender_ID (int): 장비를 등록한 Lender의 사용자 ID.
  * rental_price (decimal(10,2)): 장비 대여 가격.
  * availability (enum): 장비의 거래 상태 (대여 가능, 예약 중, 대여 중).
  * item_condition (enum): 장비의 품질 (최상, 상, 중상, 중, 중하, 하).
  * rating (float, Default 0): 장비의 평균 평점.
  * region (varchar(50)): 장비가 등록된 지역.
* 제약 조건
  * equip_ID: Primary Key.
  * lender_ID: user 테이블의 ID를 참조하는 Foreign Key.

### 3. equipment_reviews 테이블
* 기능
  * 장비 리뷰 데이터를 관리하기 위한 테이블로, Borrower가 작성한 장비의 평점 및 코멘트를 저장.
* 컬럼
  * review_ID (int, Primary Key, AUTO_INCREMENT): 리뷰 고유 ID.
  * equip_ID (int): 리뷰 대상 장비의 ID.
  * borrower_ID (int): 리뷰를 작성한 Borrower의 사용자 ID.
  * review_score (int): 장비 품질 점수 (1~6).
  * comment (text): 리뷰 코멘트.
* 제약 조건
  * equip_ID: equipment 테이블의 equip_ID를 참조하는 Foreign Key.
  * borrower_ID: user 테이블의 ID를 참조하는 Foreign Key.

### 4. message 테이블
* 기능
  * Lender와 Borrower 간의 메시지 데이터를 관리하기 위한 테이블.
* 컬럼
  * message_ID (int, Primary Key, AUTO_INCREMENT): 메시지 고유 ID.
  * conversation_ID (int): 대화 고유 ID.
  * sender_ID (int): 메시지를 보낸 사용자 ID.
  * receiver_ID (int): 메시지를 받은 사용자 ID.
  * equip_ID (int): 메시지와 관련된 장비의 ID.
  * content (text): 메시지 내용.
  * is_read (tinyint(1), Default 0): 메시지 읽음 여부.
  * created_at (timestamp): 메시지 생성 시간.
* 제약 조건
  * sender_ID, receiver_ID: user 테이블의 ID를 참조하는 Foreign Key.
  * equip_ID: equipment 테이블의 equip_ID를 참조하는 Foreign Key.

### 5. rentaltransaction 테이블
* 기능
  * 장비 대여 관련 거래 데이터를 관리하기 위한 테이블로, Lender와 Borrower 간의 거래 상태, 리뷰 정보 등을 저장.
* 컬럼
  * transaction_ID (int, Primary Key, AUTO_INCREMENT): 거래 고유 ID.
  * equip_ID (int): 거래 대상 장비 ID.
  * borrower_ID (int): 거래를 요청한 Borrower ID.
  * lender_ID (int): 거래를 수락한 Lender ID.
  * status (enum): 거래 상태 (대여 가능, 예약 중, 대여 중).
  * transaction_time (timestamp): 거래 생성 시간.
  * review_comment (text): 리뷰 코멘트.
  * review_rating (float): 거래에 대한 리뷰 평점.
* 제약 조건
  * equip_ID: equipment 테이블의 equip_ID를 참조하는 Foreign Key.
  * borrower_ID, lender_ID: user 테이블의 ID를 참조하는 Foreign Key.

### 6. unavailabledates 테이블
* 기능
  * 장비의 대여 불가능 날짜를 관리하기 위한 테이블.
* 컬럼
  * date_ID (int, Primary Key, AUTO_INCREMENT): 불가능 날짜 ID.
  * equip_ID (int): 대여 불가능 날짜와 관련된 장비 ID.
  * unavailable_date (date): 대여 불가능 날짜.
* 제약 조건
  * equip_ID: equipment 테이블의 equip_ID를 참조하는 Foreign Key.

### 7. user_reviews 테이블
* 기능
  * 사용자 간의 리뷰 데이터를 관리하기 위한 테이블로, Lender와 Borrower 간의 상호 평점 및 코멘트를 저장.
* 컬럼
  * review_ID (int, Primary Key, AUTO_INCREMENT): 리뷰 고유 ID.
  * reviewer_ID (int): 리뷰 작성자 ID.
  * reviewee_ID (int): 리뷰 대상 사용자 ID.
  * rating (int): 사용자 평점 (0~5).
  * comment (text): 리뷰 코멘트.
  * created_at (timestamp): 리뷰 작성 시간.
* 제약 조건
  * reviewer_ID, reviewee_ID: user 테이블의 ID를 참조하는 Foreign Key.
