import bcrypt
from getpass import getpass
import pymysql

def connect_db():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='cotton0010s!',
        database='CommunityRental',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def create_admin_account():
    db = connect_db()
    cursor = db.cursor()
    try:
        print("\n=== Admin 계정 생성 ===")
        name = input("Admin 이름: ").strip()
        contact = input("연락처: ").strip()
        password = getpass("비밀번호: ").strip()
        hashed_pw = hash_password(password)

        region = "서울"
        
        cursor.execute("""
            INSERT INTO User (name, contact, password, region, is_admin)
            VALUES (%s, %s, %s, %s, 1)
        """, (name, contact, hashed_pw, region))
        db.commit()
        print("\nAdmin 계정이 성공적으로 생성되었습니다.")
    except Exception as e:
        print(f"오류 발생: {e}")
    finally:
        cursor.close()
        db.close()

if __name__ == "__main__":
    create_admin_account()
