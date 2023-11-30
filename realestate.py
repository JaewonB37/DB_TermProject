import pymysql
from sshtunnel import SSHTunnelForwarder
from prettytable import PrettyTable

# # SSH 및 데이터베이스 설정
# SSH_HOST = ''
# SSH_PORT = 
# SSH_USERNAME = ''
# SSH_PASSWORD = ''
# DB_HOST = ''
# DB_USER = 'root'
# DB_PASSWORD = ''
# DB_NAME = 'estate'
# DB_PORT = 


def main_menu():
    with SSHTunnelForwarder(
            (SSH_HOST, SSH_PORT),
            ssh_username=SSH_USERNAME,
            ssh_password=SSH_PASSWORD,
            remote_bind_address=(DB_HOST, DB_PORT)) as tunnel:

        conn = pymysql.connect(host='127.0.0.1', user=DB_USER, passwd=DB_PASSWORD, db=DB_NAME, port=tunnel.local_bind_port)
        
        while True:
            display_menu()
            choice = input("메뉴 번호를 입력하세요: ")

            if choice == "0":
                break
            elif choice == "1":
                display_properties(conn)
            elif choice == "2":
                display_agents(conn)
            elif choice == "3":
                display_clients(conn)
            elif choice == "4":
                display_transactions(conn)
            elif choice == "5":
                display_appointments(conn)
            elif choice == "6":
                add_property(conn)
            elif choice == "7":
                add_agent(conn)
            elif choice == "8":
                add_client(conn)
            elif choice == "9":
                add_transaction(conn)
            elif choice == "10":
                add_appointment(conn)
            elif choice == "11":
                update_property(conn)
            elif choice == "12":
                update_agent(conn)
            elif choice == "13":
                update_client(conn)
            elif choice == "14":
                update_transaction(conn)
            elif choice == "15":
                update_appointment(conn)
            elif choice == "16":
                delete_property(conn)
            elif choice == "17":
                delete_agent(conn)
            elif choice == "18":
                delete_client(conn)
            elif choice == "19":
                delete_transaction(conn)
            elif choice == "20":
                delete_appointment(conn)
            else:
                print("잘못된 입력입니다. 다시 시도해주세요.")
        
        conn.close()


def display_menu():
    print("\n부동산 관리 시스템 메뉴:")
    print("1. 부동산 목록 조회")
    print("2. 에이전트 목록 조회")
    print("3. 고객 목록 조회")
    print("4. 거래 내역 조회")
    print("5. 예약 목록 조회")
    print("6. 부동산 추가")
    print("7. 에이전트 추가")
    print("8. 고객 추가")
    print("9. 거래 추가")
    print("10. 예약 추가")
    print("11. 부동산 정보 업데이트")
    print("12. 에이전트 정보 업데이트")
    print("13. 고객 정보 업데이트")
    print("14. 거래 정보 업데이트")
    print("15. 예약 정보 업데이트")
    print("16. 부동산 정보 삭제")
    print("17. 에이전트 정보 삭제")
    print("18. 고객 정보 삭제")
    print("19. 거래 정보 삭제")
    print("20. 예약 정보 삭제")
    print("0. 종료")


def display_properties(conn):
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM Properties")
        rows = cursor.fetchall()
        table = PrettyTable()
        table.field_names = [desc[0] for desc in cursor.description]  # 컬럼명 설정
        for row in rows:
            table.add_row(row)
        print(table)

def display_agents(conn):
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM Agents")
        rows = cursor.fetchall()
        table = PrettyTable()
        table.field_names = [desc[0] for desc in cursor.description]
        for row in rows:
            table.add_row(row)
        print("\n에이전트 목록:")
        print(table)

def display_clients(conn):
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM Clients")
        rows = cursor.fetchall()
        table = PrettyTable()
        table.field_names = [desc[0] for desc in cursor.description]
        for row in rows:
            table.add_row(row)
        print("\n고객 목록:")
        print(table)

def display_transactions(conn):
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM Transactions")
        rows = cursor.fetchall()
        table = PrettyTable()
        table.field_names = [desc[0] for desc in cursor.description]
        for row in rows:
            table.add_row(row)
        print("\n거래 내역:")
        print(table)

def display_appointments(conn):
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM Appointments")
        rows = cursor.fetchall()
        table = PrettyTable()
        table.field_names = [desc[0] for desc in cursor.description]
        for row in rows:
            table.add_row(row)
        print("\n예약 목록:")
        print(table)

def add_property(conn):
    print("\n부동산 정보 추가:")
    type = input("유형: ")
    location = input("위치: ")
    size = input("크기: ")
    price = input("가격: ")
    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO Properties (Type, Location, Size, Price) VALUES (%s, %s, %s, %s)", (type, location, size, price))
        conn.commit()
    print("부동산 정보가 추가되었습니다.")

def add_agent(conn):
    print("\n에이전트 정보 추가:")
    name = input("이름: ")
    contact_number = input("연락처: ")
    email = input("이메일: ")
    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO Agents (Name, ContactNumber, Email) VALUES (%s, %s, %s)", (name, contact_number, email))
        conn.commit()
    print("에이전트 정보가 추가되었습니다.")

def add_client(conn):
    print("\n고객 정보 추가:")
    name = input("이름: ")
    contact_number = input("연락처: ")
    email = input("이메일: ")
    address = input("주소: ")
    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO Clients (Name, ContactNumber, Email, Address) VALUES (%s, %s, %s, %s)", (name, contact_number, email, address))
        conn.commit()
    print("고객 정보가 추가되었습니다.")

def add_transaction(conn):
    print("\n거래 정보 추가:")
    property_id = input("부동산 ID: ")
    client_id = input("고객 ID: ")
    agent_id = input("에이전트 ID: ")
    date = input("거래 날짜(YYYY-MM-DD): ")
    type = input("거래 유형: ")
    amount = input("금액: ")
    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO Transactions (PropertyID, ClientID, AgentID, Date, Type, Amount) VALUES (%s, %s, %s, %s, %s, %s)", (property_id, client_id, agent_id, date, type, amount))
        conn.commit()
    print("거래 정보가 추가되었습니다.")

def add_appointment(conn):
    print("\n예약 정보 추가:")
    client_id = input("고객 ID: ")
    agent_id = input("에이전트 ID: ")
    property_id = input("부동산 ID: ")
    date = input("예약 날짜(YYYY-MM-DD): ")
    time = input("예약 시간(HH:MM): ")
    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO Appointments (ClientID, AgentID, PropertyID, Date, Time) VALUES (%s, %s, %s, %s, %s)", (client_id, agent_id, property_id, date, time))
        conn.commit()
    print("예약 정보가 추가되었습니다.")
    
def update_property(conn):
    property_id = input("수정할 부동산 ID: ")
    new_type = input("새 유형: ")
    new_location = input("새 위치: ")
    new_size = input("새 크기: ")
    new_price = input("새 가격: ")
    with conn.cursor() as cursor:
        cursor.execute("UPDATE Properties SET Type=%s, Location=%s, Size=%s, Price=%s WHERE PropertyID=%s",
                       (new_type, new_location, new_size, new_price, property_id))
        conn.commit()
        print("부동산 정보가 업데이트되었습니다.")


def update_agent(conn):
    agent_id = input("수정할 에이전트 ID: ")
    new_name = input("새 이름: ")
    new_contact_number = input("새 연락처: ")
    new_email = input("새 이메일: ")
    with conn.cursor() as cursor:
        cursor.execute("UPDATE Agents SET Name=%s, ContactNumber=%s, Email=%s WHERE AgentID=%s",
                       (new_name, new_contact_number, new_email, agent_id))
        conn.commit()
        print("에이전트 정보가 업데이트되었습니다.")

def update_client(conn):
    client_id = input("수정할 고객 ID: ")
    new_name = input("새 이름: ")
    new_contact_number = input("새 연락처: ")
    new_email = input("새 이메일: ")
    new_address = input("새 주소: ")
    with conn.cursor() as cursor:
        cursor.execute("UPDATE Clients SET Name=%s, ContactNumber=%s, Email=%s, Address=%s WHERE ClientID=%s",
                       (new_name, new_contact_number, new_email, new_address, client_id))
        conn.commit()
        print("고객 정보가 업데이트되었습니다.")

def update_transaction(conn):
    transaction_id = input("수정할 거래 ID: ")
    new_property_id = input("새 부동산 ID: ")
    new_client_id = input("새 고객 ID: ")
    new_agent_id = input("새 에이전트 ID: ")
    new_date = input("새 거래 날짜(YYYY-MM-DD): ")
    new_type = input("새 거래 유형: ")
    new_amount = input("새 금액: ")
    with conn.cursor() as cursor:
        cursor.execute("UPDATE Transactions SET PropertyID=%s, ClientID=%s, AgentID=%s, Date=%s, Type=%s, Amount=%s WHERE TransactionID=%s",
                       (new_property_id, new_client_id, new_agent_id, new_date, new_type, new_amount, transaction_id))
        conn.commit()
        print("거래 정보가 업데이트되었습니다.")

def update_appointment(conn):
    appointment_id = input("수정할 예약 ID: ")
    new_client_id = input("새 고객 ID: ")
    new_agent_id = input("새 에이전트 ID: ")
    new_property_id = input("새 부동산 ID: ")
    new_date = input("새 예약 날짜(YYYY-MM-DD): ")
    new_time = input("새 예약 시간(HH:MM): ")
    with conn.cursor() as cursor:
        cursor.execute("UPDATE Appointments SET ClientID=%s, AgentID=%s, PropertyID=%s, Date=%s, Time=%s WHERE AppointmentID=%s",
                       (new_client_id, new_agent_id, new_property_id, new_date, new_time, appointment_id))
        conn.commit()
        print("예약 정보가 업데이트되었습니다.")

def delete_property(conn):
    property_id = input("삭제할 부동산 ID: ")
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM Properties WHERE PropertyID=%s", (property_id,))
        conn.commit()
        print("부동산 정보가 삭제되었습니다.")

def delete_agent(conn):
    agent_id = input("삭제할 에이전트 ID: ")
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM Agents WHERE AgentID=%s", (agent_id,))
        conn.commit()
        print("에이전트 정보가 삭제되었습니다.")

def delete_client(conn):
    client_id = input("삭제할 고객 ID: ")
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM Clients WHERE ClientID=%s", (client_id,))
        conn.commit()
        print("고객 정보가 삭제되었습니다.")

def delete_transaction(conn):
    transaction_id = input("삭제할 거래 ID: ")
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM Transactions WHERE TransactionID=%s", (transaction_id,))
        conn.commit()
        print("거래 정보가 삭제되었습니다.")

def delete_appointment(conn):
    appointment_id = input("삭제할 예약 ID: ")
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM Appointments WHERE AppointmentID=%s", (appointment_id,))
        conn.commit()
        print("예약 정보가 삭제되었습니다.")

if __name__ == "__main__":
    main_menu()
