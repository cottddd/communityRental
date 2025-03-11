import pymysql
from getpass import getpass
from datetime import datetime
import bcrypt

# 데이터베이스 연결
def connect_db():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='cotton0010s!',
        database='CommunityRental',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

# 비밀번호 해싱
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

# 비밀번호 검증
def check_password(input_password, stored_password):
    return bcrypt.checkpw(input_password.encode('utf-8'), stored_password.encode('utf-8'))

# 사용자 등록
def register_user():
    db = connect_db()
    cursor = db.cursor()
    try:
        print("\n=== 사용자 등록 ===")
        name = input("이름: ").strip()
        contact = input("연락처: ").strip()
        password = getpass("비밀번호: ").strip()
        hashed_pw = hash_password(password).decode('utf-8')

        # 지역 선택
        print("\n지역을 선택하세요:")
        regions = ["서울", "부산", "대구", "인천", "광주", "대전", "울산"]
        for idx, region in enumerate(regions, start=1):
            print(f"{idx}. {region}")
        
        region_choice = int(input("지역 번호 입력: ").strip())
        if region_choice < 1 or region_choice > len(regions):
            print("잘못된 지역 선택입니다. 다시 시도하세요.")
            return
        region = regions[region_choice - 1]

        # 사용자 정보 삽입
        cursor.execute("""
            INSERT INTO User (name, contact, password, region)
            VALUES (%s, %s, %s, %s)
        """, (name, contact, hashed_pw, region))
        db.commit()
        print("\n사용자 등록이 완료되었습니다.")
    except Exception as e:
        print(f"오류 발생: {e}")
    finally:
        cursor.close()
        db.close()

# 로그인
def login_user():
    db = connect_db()
    cursor = db.cursor()
    print("\n=== Login ===")
    try:
        name = input("이름: ").strip()
        password = getpass("비밀번호: ").strip()

        cursor.execute("SELECT * FROM User WHERE name=%s", (name,))
        user = cursor.fetchone()

        if user and check_password(password, user["password"]):
            print(f"\n로그인 성공! {user['name']}님 환영합니다.")
            if user["is_admin"] == 1:
                admin_menu()  # Admin 메뉴로 이동
            return user
        else:
            print("\n로그인 실패. 이름과 비밀번호를 확인해주세요.")
            return None
    except Exception as e:
        print(f"오류 발생: {e}")
        return None
    finally:
        cursor.close()
        db.close()

# 관리자 메뉴
def admin_menu():
    while True:
        print("\n=== Admin Menu ===")
        print("1. 사용자 관리")
        print("2. 장비 관리")
        print("3. 리뷰 관리")
        print("0. 로그아웃")
        
        choice = input("선택: ").strip()
        if choice == "1":
            manage_users()
        elif choice == "2":
            manage_equipment_by_admin()
        elif choice == "3":
            manage_reviews_by_admin()
        elif choice == "0":
            break
        else:
            print("잘못된 선택입니다.")

# 유저 관리
def manage_users():
    db = connect_db()
    cursor = db.cursor()
    try:
        print("\n=== 사용자 관리 ===")
        print("1. 사용자 목록 보기")
        print("2. 사용자 삭제")
        print("0. 돌아가기")

        choice = input("선택: ").strip()
        if choice == "1":
            cursor.execute("SELECT ID, name, contact, region FROM User WHERE is_admin = 0")
            users = cursor.fetchall()
            if not users:
                print("등록된 사용자가 없습니다.")
                return

            print("\n=== 사용자 목록 ===")
            for user in users:
                print(f"ID: {user['ID']}, 이름: {user['name']}, 연락처: {user['contact']}, 지역: {user['region']}")

        elif choice == "2":
            user_id = input("삭제할 사용자 ID를 입력하세요: ").strip()
            cursor.execute("DELETE FROM User WHERE ID = %s AND is_admin = 0", (user_id,))
            db.commit()
            print("사용자가 성공적으로 삭제되었습니다.")

        elif choice == "0":
            return

        else:
            print("잘못된 선택입니다.")
    except Exception as e:
        print(f"오류 발생: {e}")
    finally:
        cursor.close()
        db.close()

# 관리자_장비 관리
def manage_equipment_by_admin():
    db = connect_db()
    cursor = db.cursor()
    try:
        print("\n=== 장비 관리 ===")
        cursor.execute("SELECT equip_ID, name, category, lender_ID FROM Equipment")
        equipments = cursor.fetchall()
        if not equipments:
            print("등록된 장비가 없습니다.")
            return

        print("\n=== 장비 목록 ===")
        for equip in equipments:
            print(f"ID: {equip['equip_ID']}, 이름: {equip['name']}, 카테고리: {equip['category']}, Lender ID: {equip['lender_ID']}")

        equip_id = input("삭제할 장비 ID를 입력하세요 (0은 취소): ").strip()
        if equip_id == "0":
            return

        cursor.execute("DELETE FROM Equipment WHERE equip_ID = %s", (equip_id,))
        db.commit()
        print("장비가 성공적으로 삭제되었습니다.")
    except Exception as e:
        print(f"오류 발생: {e}")
    finally:
        cursor.close()
        db.close()

# 관리자_리뷰 관리
def manage_reviews_by_admin():
    db = connect_db()
    cursor = db.cursor()
    try:
        print("\n=== 리뷰 관리 ===")
        cursor.execute("""
            SELECT rt.transaction_ID, rt.equipment_comment, rt.borrower_comment, e.name AS equip_name, u.name AS borrower_name
            FROM RentalTransaction rt
            JOIN Equipment e ON rt.equip_ID = e.equip_ID
            JOIN User u ON rt.borrower_ID = u.ID
            WHERE rt.equipment_comment IS NOT NULL OR rt.borrower_comment IS NOT NULL
        """)
        reviews = cursor.fetchall()

        if not reviews:
            print("등록된 리뷰가 없습니다.")
            return

        print("\n=== 리뷰 목록 ===")
        for review in reviews:
            print(f"거래 ID: {review['transaction_ID']}, 장비 이름: {review['equip_name']}, Borrower: {review['borrower_name']}")
            print(f"장비 리뷰: {review['equipment_comment']}")
            print(f"Borrower 리뷰: {review['borrower_comment']}")
            print("-" * 40)

        transaction_id = input("삭제할 리뷰의 거래 ID를 입력하세요 (0은 취소): ").strip()
        if transaction_id == "0":
            return

        cursor.execute("""
            UPDATE RentalTransaction
            SET equipment_comment = NULL, borrower_comment = NULL
            WHERE transaction_ID = %s
        """, (transaction_id,))
        db.commit()
        print("리뷰가 성공적으로 삭제되었습니다.")
    except Exception as e:
        print(f"오류 발생: {e}")
    finally:
        cursor.close()
        db.close()

# 대여 불가능 날짜
def add_unavailable_dates(equip_id, dates):
    db = connect_db()
    cursor = db.cursor()
    try:
        for date in dates:
            cursor.execute("""
                INSERT INTO UnavailableDates (equip_ID, unavailable_date)
                VALUES (%s, %s)
            """, (equip_id, date))
        db.commit()
        print("대여 불가능 날짜가 성공적으로 추가되었습니다.")
    except Exception as e:
        print(f"오류 발생: {e}")
    finally:
        cursor.close()
        db.close()

# 장비 등록
def add_equipment(current_user):
    db = connect_db()
    cursor = db.cursor()
    try:
        # 카테고리 데이터 정의
        categories = {
            "텐트": ["거실형/돔형텐트", "루프탑텐트", "백패킹텐트", "타프", "기타"],
            "침낭, 매트": ["침낭", "에어매트", "전기매트", "카페트/담요/러그", "베개/방석/쿠션", "기타"],
            "퍼니처": ["테이블", "체어", "해먹/스탠드", "기타"],
            "라이팅": ["스토브", "가스/오일랜턴", "LED랜턴/충전식랜턴", "기타"],
            "화로, BBQ": ["화로대", "그릴/플레이트", "가스/연료/착화제", "BBQ용품", "기타"],
            "키친": ["냄비/팬/솥/더치오븐", "수저/칼/도마/조리도구", "컵/잔/시에라", "쿨러/아이스박스/스탠드", "보온보냉병/물통/워터저그", "기타"],
            "냉난방": ["쿨러/선풍기/서큘레이터", "화목난로/등유/가스난로", "기타"],
            "스토리지": ["대형수납케이스", "소형수납케이스", "대형가방(20L 이상)", "소형가방(20L 미만)", "기타"],
            "RV용품": ["트레일러", "루프탑텐트", "루프백/루프박스", "차량용에어매트", "기타"],
            "공구": ["망치", "톱", "삽", "도끼", "나이프", "기타"]
        }

        # 상위 카테고리 선택
        print("\n상위 카테고리:")
        category_keys = list(categories.keys())
        for idx, category in enumerate(category_keys, start=1):
            print(f"{idx}. {category}")

        parent_choice = int(input("\n상위 카테고리를 선택하세요 (번호 입력): "))
        if parent_choice < 1 or parent_choice > len(category_keys):
            print("잘못된 선택입니다. 메인 메뉴로 돌아갑니다.")
            return

        parent_category = category_keys[parent_choice - 1]

        # 세부 카테고리 선택
        print(f"\n{parent_category}의 세부 카테고리:")
        subcategories = categories[parent_category]
        for idx, subcategory in enumerate(subcategories, start=1):
            print(f"{idx}. {subcategory}")

        sub_choice = int(input("\n세부 카테고리를 선택하세요 (번호 입력): "))
        if sub_choice < 1 or sub_choice > len(subcategories):
            print("잘못된 선택입니다. 메인 메뉴로 돌아갑니다.")
            return

        sub_category = subcategories[sub_choice - 1]

        # 장비 정보 입력
        name = input("장비 이름: ").strip()
        print("품질:")
        qualities = ["최상", "상", "중상", "중", "중하", "하"]
        for idx, quality in enumerate(qualities, start=1):
            print(f"{idx}. {quality}")

        quality_choice = int(input("품질을 선택하세요 (1-6): ").strip())
        if quality_choice < 1 or quality_choice > len(qualities):
            print("잘못된 선택입니다. 메인 메뉴로 돌아갑니다.")
            return

        # 품질 설정
        item_condition = qualities[quality_choice - 1]

        rental_price = float(input("대여 가격: "))
        if rental_price < 0:
            print("대여 가격은 0 이상이어야 합니다.")
            return

        # 지역 정보 추가
        region = current_user["region"]
        availability = "대여 가능"

        cursor.execute("""
            INSERT INTO Equipment (category, name, lender_ID, rental_price, item_condition, availability, region)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (f"{parent_category} - {sub_category}", name, current_user['ID'], rental_price, item_condition, availability, region))
        db.commit()
        equip_id = cursor.lastrowid

        # 대여 불가능 날짜 입력
        unavailable_dates = input("대여 불가능 날짜 (YYYY-MM-DD 형식, 쉼표로 구분, 없으면 엔터): ").strip()
        if unavailable_dates:
            dates = [date.strip() for date in unavailable_dates.split(",")]
            add_unavailable_dates(equip_id, dates)

        print(f"\n장비 '{name}'이(가) '{parent_category} - {sub_category}' 카테고리에 성공적으로 등록되었습니다.")
    except Exception as e:
        print(f"오류 발생: {e}")
    finally:
        cursor.close()
        db.close()

# 장비 검색
def search_equipment(current_user):
    db = connect_db()
    cursor = db.cursor()
    try:
        # 현재 사용자의 지역 가져오기
        cursor.execute("SELECT region FROM User WHERE ID = %s", (current_user['ID'],))
        user_region = cursor.fetchone()['region']
        print(f"현재 지역: {user_region}\n")

        # 카테고리 데이터 정의
        categories = {
            "텐트": ["거실형/돔형텐트", "루프탑텐트", "백패킹텐트", "타프", "기타"],
            "침낭, 매트": ["침낭", "에어매트", "전기매트", "카페트/담요/러그", "베개/방석/쿠션", "기타"],
            "퍼니처": ["테이블", "체어", "해먹/스탠드", "기타"],
            "라이팅": ["스토브", "가스/오일랜턴", "LED랜턴/충전식랜턴", "기타"],
            "화로, BBQ": ["화로대", "그릴/플레이트", "가스/연료/착화제", "BBQ용품", "기타"],
            "키친": ["냄비/팬/솥/더치오븐", "수저/칼/도마/조리도구", "컵/잔/시에라", "쿨러/아이스박스/스탠드", "보온보냉병/물통/워터저그", "기타"],
            "냉난방": ["쿨러/선풍기/서큘레이터", "화목난로/등유/가스난로", "기타"],
            "스토리지": ["대형수납케이스", "소형수납케이스", "대형가방(20L 이상)", "소형가방(20L 미만)", "기타"],
            "RV용품": ["트레일러", "루프탑텐트", "루프백/루프박스", "차량용에어매트", "기타"],
            "공구": ["망치", "톱", "삽", "도끼", "나이프", "기타"]
        }

        print("검색 기준을 선택하세요:")
        print("1. 카테고리 검색")
        print("2. 이름 검색")
        search_choice = int(input("선택 (1 또는 2): "))

        if search_choice == 1:
            # 상위 카테고리 출력
            print("\n상위 카테고리:")
            category_keys = list(categories.keys())
            for idx, category in enumerate(category_keys, start=1):
                print(f"{idx}. {category}")

            # 상위 카테고리 선택
            parent_choice = int(input("\n상위 카테고리를 선택하세요 (번호 입력): "))
            if parent_choice < 1 or parent_choice > len(category_keys):
                print("잘못된 선택입니다. 메인 메뉴로 돌아갑니다.")
                return None

            parent_category = category_keys[parent_choice - 1]

            # 세부 카테고리 출력
            print(f"\n{parent_category}의 세부 카테고리:")
            subcategories = categories[parent_category]
            for idx, subcategory in enumerate(subcategories, start=1):
                print(f"{idx}. {subcategory}")

            # 세부 카테고리 선택
            sub_choice = int(input("\n세부 카테고리를 선택하세요 (번호 입력): "))
            if sub_choice < 1 or sub_choice > len(subcategories):
                print("잘못된 선택입니다. 메인 메뉴로 돌아갑니다.")
                return None

            sub_category = subcategories[sub_choice - 1]
            full_category = f"{parent_category} - {sub_category}"

            # 장비 검색
            cursor.execute("""
                SELECT e.equip_ID, e.name, e.category, e.item_condition, e.rental_price, e.lender_ID,
                       GROUP_CONCAT(DATE_FORMAT(ud.unavailable_date, '%%Y-%%m-%%d') ORDER BY ud.unavailable_date ASC) AS unavailable_dates
                FROM Equipment e
                LEFT JOIN UnavailableDates ud ON e.equip_ID = ud.equip_ID
                WHERE e.category = %s AND e.region = %s
                GROUP BY e.equip_ID
            """, (full_category, user_region))
            equipments = cursor.fetchall()

        elif search_choice == 2:
            keyword = input("검색할 장비 이름 또는 키워드를 입력하세요: ").strip()
            cursor.execute("""
                SELECT e.equip_ID, e.name, e.category, e.item_condition, e.rental_price, e.lender_ID,
                       GROUP_CONCAT(DATE_FORMAT(ud.unavailable_date, '%%Y-%%m-%%d') ORDER BY ud.unavailable_date ASC) AS unavailable_dates
                FROM Equipment e
                LEFT JOIN UnavailableDates ud ON e.equip_ID = ud.equip_ID
                WHERE e.name LIKE %s AND e.region = %s
                GROUP BY e.equip_ID
            """, ('%' + keyword + '%', user_region))
            equipments = cursor.fetchall()

        else:
            print("잘못된 선택입니다. 메인 메뉴로 돌아갑니다.")
            return None

        # 검색 결과 출력
        if not equipments:
            print("\n검색 결과가 없습니다.")
            return None

        print("\n=== Search Results ===")
        for idx, equipment in enumerate(equipments, start=1):
            print(f"{idx}. {equipment['name']} (카테고리: {equipment['category']}, 상태: {equipment['item_condition']}, "
                  f"대여 불가능 날짜: {equipment['unavailable_dates'] if equipment['unavailable_dates'] else '없음'})")

        # 장비 선택
        choice = int(input("세부 정보를 확인할 장비를 선택하세요 (번호 입력, 0은 메인 메뉴로): "))
        if choice == 0:
            return None

        selected_equipment = equipments[choice - 1]
        view_equipment_details(selected_equipment['equip_ID'], current_user)

    except Exception as e:
        print(f"오류 발생: {e}")
    finally:
        cursor.close()
        db.close()

# 메시지 보내기
def send_message(sender_id, receiver_id, equip_id, content, conversation_id=None):
    db = connect_db()
    cursor = db.cursor()
    try:
        if not receiver_id:
            raise ValueError("수신자 ID(receiver_ID)가 누락되었습니다.")

        # 기존 거래 확인 및 생성
        cursor.execute("""
            SELECT transaction_ID
            FROM RentalTransaction
            WHERE equip_ID = %s AND borrower_ID = %s AND lender_ID = %s
        """, (equip_id, sender_id, receiver_id))
        transaction = cursor.fetchone()

        if not transaction:
            cursor.execute("""
                INSERT INTO RentalTransaction (equip_ID, borrower_ID, lender_ID, status)
                VALUES (%s, %s, %s, '대여 가능')
            """, (equip_id, sender_id, receiver_id))
            db.commit()

        # 메시지 삽입
        if conversation_id is None:
            cursor.execute("SELECT MAX(conversation_ID) FROM Message;")
            result = cursor.fetchone()
            conversation_id = (result['MAX(conversation_ID)'] or 0) + 1

        cursor.execute("""
            INSERT INTO Message (conversation_ID, sender_ID, receiver_ID, equip_ID, content)
            VALUES (%s, %s, %s, %s, %s)
        """, (conversation_id, sender_id, receiver_id, equip_id, content))
        db.commit()
        print("메시지가 성공적으로 전송되었습니다.")

    except Exception as e:
        print(f"오류 발생: {e}")
    finally:
        cursor.close()
        db.close()


# 리뷰 등록
def prompt_review(user_id, transaction_id, role):
    db = connect_db()
    cursor = db.cursor()
    try:
        if role == "borrower":
            cursor.execute("""
            SELECT lender_ID FROM RentalTransaction WHERE transaction_ID = %s
            """, (transaction_id,))
            lender_id = cursor.fetchone()["lender_ID"]

            # Borrower 자신인지 확인
            if user_id == lender_id:
                print("자신에게 리뷰를 작성할 수 없습니다.")
                return

            print("\n장비에 대한 리뷰를 작성하시겠습니까? (Y/N): ", end="")
            if input().strip().upper() != "Y":
                print("리뷰 작성이 생략되었습니다.")
                return

            # 장비 리뷰 작성
            equipment_quality = input("장비의 상태는 어땠나요? (최상/상/중상/중/중하/하): ").strip()
            quality_map = {"최상": 6, "상": 5, "중상": 4, "중": 3, "중하": 2, "하": 1}
            quality_score = quality_map.get(equipment_quality)
            if quality_score is None:
                print("올바른 품질을 선택해주세요.")
                return

            equipment_comment = input("장비 품질에 대하여 리뷰를 남겨주세요: ").strip()

            # Lender 거래 리뷰
            lender_rating = int(input(f"Lender님과의 거래는 어땠나요? (0~5점): ").strip())
            lender_comment = input(f"Lender님과의 거래에 대하여 리뷰를 남겨주세요: ").strip()

            cursor.execute("""
            UPDATE RentalTransaction
            SET equipment_quality_review = %s, equipment_comment = %s, lender_rating = %s, lender_comment = %s, review_completed = 1
            WHERE transaction_ID = %s
            """, (quality_score, equipment_comment, lender_rating, lender_comment, transaction_id))
            db.commit()
            print("장비 리뷰와 거래 리뷰가 성공적으로 등록되었습니다.")

        elif role == "lender":
            print("\nBorrower에 대한 리뷰를 작성하시겠습니까? (Y/N): ", end="")
            if input().strip().upper() != "Y":
                print("리뷰 작성이 생략되었습니다.")
                return

            borrower_rating = int(input("Borrower 평점 (0~5): ").strip())
            borrower_comment = input("Borrower에 대한 코멘트를 작성하세요: ").strip()

            cursor.execute("""
            UPDATE RentalTransaction
            SET borrower_rating = %s, borrower_comment = %s
            WHERE transaction_ID = %s
            """, (borrower_rating, borrower_comment, transaction_id))
            db.commit()
            print("Borrower에 대한 리뷰가 성공적으로 등록되었습니다.")
    except Exception as e:
        print(f"오류 발생: {e}")
    finally:
        cursor.close()
        db.close()

# 메시지 리스트 보기
def view_message_list(user_id):
    db = connect_db()
    cursor = db.cursor()
    try:
        cursor.execute("""
            SELECT m.conversation_ID, 
                   u.name AS other_user, 
                   MAX(m.created_at) AS last_time, 
                   SUBSTRING_INDEX(MAX(CONCAT(m.created_at, '|', m.content)), '|', -1) AS last_message
            FROM Message m
            JOIN User u ON u.ID = (CASE WHEN m.sender_ID = %s THEN m.receiver_ID ELSE m.sender_ID END)
            WHERE m.sender_ID = %s OR m.receiver_ID = %s
            GROUP BY m.conversation_ID, u.name
            ORDER BY last_time DESC
        """, (user_id, user_id, user_id))
        conversations = cursor.fetchall()

        if not conversations:
            print("현재 메시지가 없습니다.")
            return None

        print("\n=== Message List ===")
        for convo in conversations:
            print(f"대화 ID: {convo['conversation_ID']}, 상대: {convo['other_user']}, 마지막 메시지: {convo['last_message']}")

        conversation_id = int(input("대화 ID를 선택하세요 (0은 메인 메뉴로 돌아가기): "))
        if conversation_id == 0:
            return None
        return conversation_id
    except Exception as e:
        print(f"오류 발생: {e}")
        return None
    finally:
        cursor.close()
        db.close()

def view_conversation(conversation_id, user_id):
    db = connect_db()
    cursor = db.cursor()
    try:
        # 메시지 기록 조회
        cursor.execute("""
            SELECT m.message_ID, m.content, m.reply, m.created_at, u.name AS sender_name, m.sender_ID, m.receiver_ID, m.equip_ID
            FROM Message m
            JOIN User u ON m.sender_ID = u.ID
            WHERE m.conversation_ID = %s
            ORDER BY m.created_at ASC
        """, (conversation_id,))
        messages = cursor.fetchall()

        if not messages:
            print("해당 대화에 메시지가 없습니다.")
            return

        # 거래 정보 가져오기
        equip_id = messages[0]['equip_ID']
        cursor.execute("""
            SELECT rt.transaction_ID, rt.status, rt.borrower_ID, u1.name AS borrower_name,
                   rt.lender_ID, u2.name AS lender_name, e.availability, e.name AS equip_name, e.equip_ID
            FROM RentalTransaction rt
            JOIN User u1 ON rt.borrower_ID = u1.ID
            JOIN User u2 ON rt.lender_ID = u2.ID
            JOIN Equipment e ON rt.equip_ID = e.equip_ID
            WHERE rt.equip_ID = %s AND (rt.borrower_ID = %s OR rt.lender_ID = %s)
        """, (equip_id, user_id, user_id))
        transaction = cursor.fetchone()

        if not transaction:
            print("이 대화에 접근할 권한이 없습니다.")
            return

        # 메시지 출력
        print("\n=== Conservation ===")
        for msg in messages:
            print(f"[{msg['created_at']}] {msg['sender_name']}: {msg['content']}")

        # 답장 작성
        reply = input("답장을 입력하세요 (엔터는 답장 생략, 1: 리뷰 확인): ").strip()
        if reply == "1":
            review_target_id = transaction["borrower_ID"] if user_id == transaction["lender_ID"] else transaction["lender_ID"]
            view_user_reviews(review_target_id)
            return
        elif reply:
            receiver_id = (
                transaction['borrower_ID']
                if user_id == transaction['lender_ID']
                else transaction['lender_ID']
            )
            cursor.execute("""
                INSERT INTO Message (conversation_ID, sender_ID, receiver_ID, equip_ID, content, reply)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (conversation_id, user_id, receiver_id, equip_id, reply, None))
            db.commit()
            print("답장이 성공적으로 전송되었습니다.")

        # 거래 상태 변경
        current_status = transaction["status"]
        if current_status == "대여 가능" and user_id == transaction["lender_ID"]:
            if input("장비를 '예약 중' 상태로 변경하시겠습니까? (Y/N): ").strip().upper() == "Y":
                update_equipment_status(transaction["equip_ID"], "예약 중", transaction["transaction_ID"])
                print("거래 상태가 '예약 중'으로 변경되었습니다.")

        elif current_status == "예약 중" and user_id == transaction["borrower_ID"]:
            if input("장비를 '대여 중' 상태로 변경하시겠습니까? (Y/N): ").strip().upper() == "Y":
                update_equipment_status(transaction["equip_ID"], "대여 중", transaction["transaction_ID"])
                print("거래 상태가 '대여 중'으로 변경되었습니다.")

        elif current_status == "대여 중" and user_id == transaction["borrower_ID"]:
            if input("거래 상태를 '반납 완료'로 변경하시겠습니까? (Y/N): ").strip().upper() == "Y":
                update_equipment_status(transaction["equip_ID"], "대여 가능", transaction["transaction_ID"])
                print("거래 상태가 '대여 가능'으로 변경되었습니다.")

                # 채팅창에 거래 상태 변경 메시지 추가
                cursor.execute("""
                    INSERT INTO Message (conversation_ID, sender_ID, receiver_ID, equip_ID, content)
                    VALUES (%s, %s, %s, %s, %s)
                """, (conversation_id, user_id, transaction["lender_ID"], equip_id,
                      f"{transaction['borrower_name']}님이 대여를 끝냈습니다."))
                db.commit()

                # 장비 리뷰 작성 요청
                borrower_review_now = input(f"\n장비 '{transaction['equip_name']}'에 대한 리뷰를 작성하시겠습니까? (Y/N): ").strip().upper()
                if borrower_review_now == "Y":
                    prompt_review(user_id, transaction["transaction_ID"], role="borrower")

    except Exception as e:
        print(f"오류 발생: {e}")
    finally:
        cursor.close()
        db.close()

# 장비 상태 변경
def update_equipment_status(equip_id, new_status, transaction_id=None):
    db = connect_db()
    cursor = db.cursor()
    try:
        # 장비 상태 업데이트
        cursor.execute("""
            UPDATE Equipment
            SET availability = %s
            WHERE equip_ID = %s
        """, (new_status, equip_id))
        db.commit()

        # 거래 상태 업데이트
        if transaction_id:
            valid_statuses = ['예약 중', '대여 중', '대여 가능']
            if new_status not in valid_statuses:
                raise ValueError(f"잘못된 거래 상태 값: {new_status}")

            cursor.execute("""
                UPDATE RentalTransaction
                SET status = %s
                WHERE transaction_ID = %s
            """, (new_status, transaction_id))
            db.commit()

    except Exception as e:
        print(f"오류 발생: {e}")
    finally:
        cursor.close()
        db.close()

# 메시지 읽기 및 답장
def view_and_reply_messages(user_id):
    db = connect_db()
    cursor = db.cursor()
    try:
        # 받은 메시지 조회
        cursor.execute("""
            SELECT m.message_ID, u.name AS sender_name, e.name AS equip_name, m.content, m.reply, m.is_read, m.created_at, e.equip_ID
            FROM Message m
            JOIN User u ON m.sender_ID = u.ID
            JOIN Equipment e ON m.equip_ID = e.equip_ID
            WHERE m.receiver_ID = %s
        """, (user_id,))
        messages = cursor.fetchall()

        if not messages:
            print("새 메시지가 없습니다.")
            return

        print("\n=== Message ===")
        for message in messages:
            read_status = "읽음" if message['is_read'] else "읽지 않음"
            print(f"""
                메시지 ID: {message['message_ID']}
                보낸 사람: {message['sender_name']}
                장비 이름: {message['equip_name']}
                내용: {message['content']}
                답장: {message['reply'] if message['reply'] else "없음"}
                상태: {read_status}
                보낸 시간: {message['created_at']}
                """)

        # 메시지 읽기 및 답장
        message_id = int(input("답장할 메시지 ID를 선택하세요 (0은 취소): "))
        if message_id == 0:
            return
        selected_message = next((msg for msg in messages if msg['message_ID'] == message_id), None)
        if not selected_message:
            print("잘못된 메시지 ID입니다.")
            return

        reply_content = input("답장 내용을 입력하세요: ")
        reply_to_message(message_id, reply_content)

        # 장비 상태 변경
        change_status = input("장비를 '예약 중' 상태로 변경하시겠습니까? (Y/N): ").upper()
        if change_status == "Y":
            update_equipment_status(selected_message['equip_ID'], '예약 중')

    except Exception as e:
        print(f"오류 발생: {e}")
    finally:
        cursor.close()
        db.close()

# Borrower가 장비 대여 중으로 변경
def confirm_rental(equip_id):
    db = connect_db()
    cursor = db.cursor()
    try:
        update_equipment_status(equip_id, '대여 중')
    except Exception as e:
        print(f"오류 발생: {e}")
    finally:
        cursor.close()
        db.close()

# 장비 품질 평균 업데이트
def update_equipment_rating(equip_id):
    db = connect_db()
    cursor = db.cursor()
    try:
        cursor.execute("""
            SELECT AVG(review_score) AS avg_rating, COUNT(*) AS total_reviews
            FROM equipment_reviews
            WHERE equip_ID = %s
        """, (equip_id,))
        result = cursor.fetchone()
        avg_rating = round(result['avg_rating'], 1) if result['avg_rating'] else 0
        total_reviews = result['total_reviews'] if result['total_reviews'] else 0

        cursor.execute("""
            UPDATE equipment
            SET rating = %s, rating_count = %s
            WHERE equip_ID = %s
        """, (avg_rating, total_reviews, equip_id))
        db.commit()
    except Exception as e:
        print(f"오류 발생: {e}")
    finally:
        cursor.close()
        db.close()

# 장비 리뷰 작성
def write_equipment_review(transaction_id, borrower_id):
    db = connect_db()
    cursor = db.cursor()
    try:
        cursor.execute("""
            SELECT equip_ID
            FROM rentaltransaction
            WHERE transaction_ID = %s
        """, (transaction_id,))
        equip = cursor.fetchone()
        if not equip:
            print("거래를 찾을 수 없습니다.")
            return

        equip_id = equip['equip_ID']
        score = int(input("장비 품질 평점 (1-6): "))
        if score < 1 or score > 6:
            print("올바른 평점을 입력해주세요.")
            return

        comment = input("장비 리뷰 코멘트를 작성하세요: ")

        cursor.execute("""
            INSERT INTO equipment_reviews (equip_ID, borrower_ID, review_score, comment)
            VALUES (%s, %s, %s, %s)
        """, (equip_id, borrower_id, score, comment))
        db.commit()

        update_equipment_rating(equip_id)
        print("장비 리뷰가 성공적으로 등록되었습니다.")
    except Exception as e:
        print(f"오류 발생: {e}")
    finally:
        cursor.close()
        db.close()

#유저 리뷰 작성
def write_user_review(reviewer_id, reviewee_id):
    db = connect_db()
    cursor = db.cursor()
    try:
        rating = int(input("유저 평점 (0-5): "))
        if rating < 0 or rating > 5:
            print("올바른 평점을 입력해주세요.")
            return

        comment = input("유저 리뷰 코멘트를 작성하세요: ")

        cursor.execute("""
            INSERT INTO user_reviews (reviewer_ID, reviewee_ID, rating, comment)
            VALUES (%s, %s, %s, %s)
        """, (reviewer_id, reviewee_id, rating, comment))
        db.commit()

        print("유저 리뷰가 성공적으로 등록되었습니다.")
    except Exception as e:
        print(f"오류 발생: {e}")
    finally:
        cursor.close()
        db.close()

# 장비 리뷰 보기
def view_equipment_reviews(equip_id):
    db = connect_db()
    cursor = db.cursor()
    try:
        cursor.execute("""
            SELECT rt.equipment_quality_review, rt.equipment_comment
            FROM RentalTransaction rt
            WHERE rt.equip_ID = %s AND rt.equipment_quality_review IS NOT NULL
        """, (equip_id,))
        reviews = cursor.fetchall()

        if not reviews:
            print("이 장비에 대한 리뷰가 없습니다.")
            return

        print("\n=== Equipment Reviews ===")
        for review in reviews:
            print(f"품질: {review['equipment_quality_review']}, 코멘트: {review['equipment_comment']}")
    except Exception as e:
        print(f"오류 발생: {e}")
    finally:
        cursor.close()
        db.close()

# 유저 리뷰 보기
def view_user_reviews(user_id):
    db = connect_db()
    cursor = db.cursor()
    try:
        # Lender와 Borrower에 대한 리뷰를 모두 가져오기
        cursor.execute("""
            SELECT rt.lender_rating AS rating, rt.lender_comment AS comment, rt.transaction_time AS created_at, u.name AS reviewer_name
            FROM RentalTransaction rt
            JOIN User u ON rt.borrower_ID = u.ID
            WHERE rt.lender_ID = %s AND rt.lender_rating IS NOT NULL
            UNION
            SELECT rt.borrower_rating AS rating, rt.borrower_comment AS comment, rt.transaction_time AS created_at, u.name AS reviewer_name
            FROM RentalTransaction rt
            JOIN User u ON rt.lender_ID = u.ID
            WHERE rt.borrower_ID = %s AND rt.borrower_rating IS NOT NULL
            ORDER BY created_at DESC
        """, (user_id, user_id))
        reviews = cursor.fetchall()

        if not reviews:
            print("이 사용자에 대한 리뷰가 없습니다.")
            return

        print("\n=== User reviews ===")
        for review in reviews:
            print(f"작성자: {review['reviewer_name']}")
            print(f"평점: {review['rating']}")
            print(f"코멘트: {review['comment']}")
            print(f"작성일: {review['created_at']}")
            print("-" * 30)
    except Exception as e:
        print(f"오류 발생: {e}")
    finally:
        cursor.close()
        db.close()

# 장비 세부사항 조회
def view_equipment_details(equip_id, current_user):
    db = connect_db()
    cursor = db.cursor()
    try:
        # 장비 세부 정보 가져오기
        cursor.execute("""
            SELECT e.equip_ID, e.name, e.category, e.item_condition, e.rental_price, e.rating, e.lender_ID, u.name AS lender_name
            FROM Equipment e
            JOIN User u ON e.lender_ID = u.ID
            WHERE e.equip_ID = %s
        """, (equip_id,))
        equipment = cursor.fetchone()

        if not equipment:
            print("장비 정보를 찾을 수 없습니다.")
            return

        print("\n=== Equipment Details ===")
        print(f"이름: {equipment['name']}")
        print(f"카테고리: {equipment['category']}")
        print(f"상태: {equipment['item_condition']}")
        print(f"대여 가격: {equipment['rental_price']:.2f}")
        print(f"Lender: {equipment['lender_name']}")

        # 장비 상세 정보 메뉴
        while True:
            print("\n1. 장비 리뷰 보기")
            print("2. Lender 리뷰 보기")
            print("3. 대여 요청 메시지 보내기")
            print("0. 돌아가기")
            
            choice = input("선택: ").strip()

            if choice == "1":
                view_equipment_reviews(equipment['equip_ID'])
            elif choice == "2":
                view_user_reviews(equipment['lender_ID'])
            elif choice == "3":
                content = input("대여 요청 메시지를 입력하세요: ").strip()
                if content:
                    send_message(
                        sender_id=current_user['ID'],
                        receiver_id=equipment['lender_ID'],
                        equip_id=equipment['equip_ID'],
                        content=content
                    )
                else:
                    print("메시지 내용이 비어 있습니다. 요청이 취소됩니다.")
                break  # 메시지 전송 후 상세 정보 화면 종료
            elif choice == "0":
                break
            else:
                print("올바른 옵션을 선택해주세요.")
    except Exception as e:
        print(f"오류 발생: {e}")
    finally:
        cursor.close()
        db.close()

def manage_equipment(lender_id):
    db = connect_db()
    cursor = db.cursor()
    try:
        # Lender가 등록한 모든 장비 조회
        cursor.execute("""
        SELECT e.equip_ID, e.name, e.category, e.item_condition, e.availability
        FROM Equipment e
        WHERE e.lender_ID = %s
        """, (lender_id,))
        equipment_list = cursor.fetchall()

        if not equipment_list:
            print("등록된 장비가 없습니다.")
            return

        print("\n=== Registered Equipment ===")
        for idx, equipment in enumerate(equipment_list, start=1):
            print(f"{idx}. {equipment['name']} (카테고리: {equipment['category']} / 품질: {equipment['item_condition']} / 거래 상태: {equipment['availability']})")
        print("0. 메인으로 돌아가기")

        choice = input("관리할 장비를 선택하세요 (번호 입력): ").strip()
        if choice == "0":
            return

        # 선택된 장비 관리
        selected_idx = int(choice) - 1
        if 0 <= selected_idx < len(equipment_list):
            selected_equip_id = equipment_list[selected_idx]['equip_ID']
            manage_selected_equipment(selected_equip_id)
        else:
            print("잘못된 선택입니다.")
    except Exception as e:
        print(f"오류 발생: {e}")
    finally:
        cursor.close()
        db.close()


def manage_selected_equipment(equip_id):
    db = connect_db()
    cursor = db.cursor()
    try:
        while True:
            # 장비 세부 정보 가져오기
            cursor.execute("""
            SELECT e.equip_ID, e.name, e.category, e.item_condition, e.rental_price, e.rating, e.availability, u.name AS lender_name
            FROM Equipment e
            JOIN User u ON e.lender_ID = u.ID
            WHERE e.equip_ID = %s
            """, (equip_id,))
            equipment = cursor.fetchone()

            if not equipment:
                print("장비 정보를 찾을 수 없습니다.")
                return

            # 대여 불가능 날짜 가져오기
            cursor.execute("""
            SELECT unavailable_date 
            FROM UnavailableDates
            WHERE equip_ID = %s
            """, (equip_id,))
            unavailable_dates = cursor.fetchall()

            # 세부 정보 출력
            print(f"\n=== Equipment Details ===")
            print(f"이름: {equipment['name']}")
            print(f"카테고리: {equipment['category']}")
            print(f"상태: {equipment['item_condition']}")
            print(f"대여 가격: {equipment['rental_price']:.2f}")
            print(f"평점: {equipment['rating']:.1f}")
            print(f"거래 상태: {equipment['availability']}")
            print(f"Lender: {equipment['lender_name']}")
            print("\n=== Rental unavailable date ===")
            if unavailable_dates:
                for date in unavailable_dates:
                    print(f"- {date['unavailable_date']}")
            else:
                print("대여 불가능 날짜가 없습니다.")

            print("\n1. 대여 날짜 추가/삭제")
            print("2. 리뷰 관리")
            print("0. 메인으로 돌아가기")

            choice = input("선택: ").strip()
            if choice == "0":
                return
            elif choice == "1":
                manage_equipment_availability(equip_id)
            elif choice == "2":
                manage_reviews(equip_id)
            else:
                print("잘못된 선택입니다. 다시 입력하세요.")
    except Exception as e:
        print(f"오류 발생: {e}")
    finally:
        cursor.close()
        db.close()


def manage_equipment_availability(equip_id):
    db = connect_db()
    cursor = db.cursor()
    try:
        while True:
            print("\n=== Equipment Availability Management ===")
            print("1. 대여 날짜 추가")
            print("2. 대여 날짜 삭제")
            print("0. 돌아가기")
            choice = input("선택: ").strip()

            if choice == "1":
                new_dates = input("추가할 대여 불가능 날짜를 입력하세요 (YYYY-MM-DD, 쉼표로 구분): ").strip()
                if new_dates:
                    dates = [date.strip() for date in new_dates.split(",")]
                    add_unavailable_dates(equip_id, dates)

            elif choice == "2":
                cursor.execute("""
                SELECT unavailable_date 
                FROM UnavailableDates 
                WHERE equip_ID = %s
                """, (equip_id,))
                unavailable_dates = cursor.fetchall()

                if not unavailable_dates:
                    print("대여 불가능 날짜가 없습니다.")
                    return

                print("\n=== Rental unavailable date ===")
                for idx, record in enumerate(unavailable_dates, start=1):
                    print(f"{idx}. {record['unavailable_date']}")
                print("0. 취소")

                delete_choice = input("삭제할 날짜의 번호를 선택하세요: ").strip()
                if delete_choice == "0":
                    return

                selected_date = unavailable_dates[int(delete_choice) - 1]["unavailable_date"]
                cursor.execute("""
                DELETE FROM UnavailableDates 
                WHERE equip_ID = %s AND unavailable_date = %s
                """, (equip_id, selected_date))
                db.commit()
                print(f"날짜 {selected_date}가 성공적으로 삭제되었습니다.")

            elif choice == "0":
                return
            else:
                print("잘못된 선택입니다. 다시 시도하세요.")
    except Exception as e:
        print(f"오류 발생: {e}")
    finally:
        cursor.close()
        db.close()


def manage_reviews(equip_id):
    db = connect_db()
    cursor = db.cursor()
    try:
        cursor.execute("""
        SELECT rt.transaction_ID, u.name AS borrower_name, MAX(m.created_at) AS last_message_date, 
               CASE WHEN rt.borrower_rating IS NOT NULL THEN '작성 완료' ELSE '미작성' END AS review_status
        FROM RentalTransaction rt
        JOIN User u ON rt.borrower_ID = u.ID
        LEFT JOIN Message m ON rt.transaction_ID = m.equip_ID
        WHERE rt.equip_ID = %s
        GROUP BY rt.transaction_ID
        """, (equip_id,))
        transactions = cursor.fetchall()

        if not transactions:
            print("리뷰 관리할 거래가 없습니다.")
            return

        print("\n=== Borrower List ===")
        for idx, transaction in enumerate(transactions, start=1):
            print(f"{idx}. {transaction['borrower_name']} (마지막 메시지: {transaction['last_message_date']}) (리뷰 상태: {transaction['review_status']})")
        print("0. 돌아가기")

        choice = input("리뷰를 관리할 Borrower를 선택하세요 (번호 입력): ").strip()
        if choice == "0":
            return

        selected_transaction = transactions[int(choice) - 1]
        if selected_transaction["review_status"] == "미작성":
            # Lender 리뷰 작성 로직
            prompt_review(
                user_id=None,  # 현재 Lender의 ID를 적절히 전달
                transaction_id=selected_transaction["transaction_ID"],
                role="lender"
            )
        else:
            print("이미 리뷰가 작성되었습니다.")
    except Exception as e:
        print(f"오류 발생: {e}")
    finally:
        cursor.close()
        db.close()

# 메인 메뉴
def main():
    while True:
        print("=== Community Rental ===")
        print("1. 사용자 등록")
        print("2. 로그인")
        print("3. 종료")
        print("----------")
        choice = input("선택: ")

        if choice == "1":
            register_user()
        elif choice == "2":
            user = login_user()
            if user:
                while True:
                    print("\n=== Main ===")
                    print("1. 장비 등록")
                    print("2. 장비 검색 및 대여 요청")
                    print("3. 메시지 확인 및 기록 보기")
                    print("4. 등록 장비  관리")
                    print("5. 로그아웃")
                    print("----------")
                    user_choice = input("선택: ")

                    if user_choice == "1":
                        add_equipment(user)
                    elif user_choice == "2":
                        search_equipment(user)
                    elif user_choice == "3":
                        conversation_id = view_message_list(user['ID'])
                        if conversation_id:
                            view_conversation(conversation_id, user['ID'])
                    elif user_choice == "4":
                        manage_equipment(user['ID'])
                    elif user_choice == "5":
                        break
                    else:
                        print("올바른 옵션을 선택해주세요.")
        elif choice == "3":
            print("프로그램을 종료합니다.")
            break
        else:
            print("올바른 옵션을 선택해주세요.")

if __name__ == "__main__":
    main()
