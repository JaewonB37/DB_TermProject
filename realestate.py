import paramiko
import mysql.connector

# SSH 서버 정보
ssh_host = "192.168.0.10"  # SSH 서버 주소
ssh_port = 22  # SSH 포트
ssh_username = "jaewon"  # SSH 사용자 이름
ssh_password = ""  # SSH 비밀번호

# SSH 터널 설정
def setup_ssh_tunnel():
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(ssh_host, port=ssh_port, username=ssh_username, password=ssh_password)
    ssh_transport = ssh_client.get_transport()
    local_port = 3306  # 로컬 포트 (MySQL과 동일한 포트)
    remote_host = "192.168.0.10"  # 원격 MySQL 호스트 (SSH 터널을 통해 접근)
    remote_port = 3306  # 원격 MySQL 포트

    # SSH 터널 열기
    ssh_channel = ssh_transport.open_channel("direct-tcpip", (remote_host, remote_port), ("localhost", local_port))
    return ssh_channel

# MySQL 연결 설정
def setup_mysql_connection(ssh_channel):
    db_connection = mysql.connector.connect(
        host="192.168.0.10",
        user="root",
        password="1234",
        database="estate",
        port=ssh_channel.getpeername()[1]  # SSH 터널로부터 포트 얻기
    )
    return db_connection

# 메뉴 표시 함수
def display_menu():
    print("부동산 관리 시스템 메뉴:")
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
    print("0. 종료")

# 메인 메뉴 함수
def main_menu():
    ssh_channel = setup_ssh_tunnel()
    db_connection = setup_mysql_connection(ssh_channel)
    cursor = db_connection.cursor()

    while True:
        display_menu()
        choice = input("메뉴 번호를 입력하세요: ")

        if choice == "0":
            break
        elif choice == "1":
            display_properties(cursor)
        elif choice == "2":
            display_agents(cursor)
        elif choice == "3":
            display_clients(cursor)
        elif choice == "4":
            display_transactions(cursor)
        elif choice == "5":
            display_appointments(cursor)
        elif choice == "6":
            add_property(cursor, db_connection)
        elif choice == "7":
            add_agent(cursor, db_connection)
        elif choice == "8":
            add_client(cursor, db_connection)
        elif choice == "9":
            add_transaction(cursor, db_connection)
        elif choice == "10":
            add_appointment(cursor, db_connection)
        else:
            print("올바른 메뉴 번호를 입력하세요.")

    # MySQL 연결 종료
    cursor.close()
    db_connection.close()
    ssh_channel.close()

# 각각의 메뉴 함수 (추가 기능)
def display_properties(cursor):
    cursor.execute("SELECT * FROM properties")
    properties = cursor.fetchall()
    print("부동산 목록:")
    for property in properties:
        print(f"Property ID: {property[0]}, Type: {property[1]}, Location: {property[2]}, Size: {property[3]}, Price: {property[4]}")

def display_agents(cursor):
    cursor.execute("SELECT * FROM agents")
    agents = cursor.fetchall()
    print("에이전트 목록:")
    for agent in agents:
        print(f"Agent ID: {agent[0]}, Name: {agent[1]}, Contact Number: {agent[2]}, Email: {agent[3]}")

def display_clients(cursor):
    cursor.execute("SELECT * FROM clients")
    clients = cursor.fetchall()
    print("고객 목록:")
    for client in clients:
        print(f"Client ID: {client[0]}, Name: {client[1]}, Contact Number: {client[2]}, Email: {client[3]}, Address: {client[4]}")

def display_transactions(cursor):
    cursor.execute("SELECT * FROM transactions")
    transactions = cursor.fetchall()
    print("거래 내역:")
    for transaction in transactions:
        print(f"Transaction ID: {transaction[0]}, Property ID: {transaction[1]}, Client ID: {transaction[2]}, Agent ID: {transaction[3]}, Date: {transaction[4]}, Type: {transaction[5]}, Amount: {transaction[6]}")

def display_appointments(cursor):
    cursor.execute("SELECT * FROM appointments")
    appointments = cursor.fetchall()
    print("예약 목록:")
    for appointment in appointments:
        print(f"Appointment ID: {appointment[0]}, Client ID: {appointment[1]}, Agent ID: {appointment[2]}, Property ID: {appointment[3]}, Date: {appointment[4]}, Time: {appointment[5]}")

def add_property(cursor, db_connection):
    prop_type = input("부동산 유형 입력: ")
    location = input("위치 입력: ")
    size = float(input("크기 입력: "))
    price = float(input("가격 입력: "))

    cursor.execute("INSERT INTO properties (Type, Location, Size, Price) VALUES (%s, %s, %s, %s)",
                   (prop_type, location, size, price))
    db_connection.commit()
    print("부동산이 추가되었습니다.")

def add_agent(cursor, db_connection):
    name = input("에이전트 이름 입력: ")
    contact_number = input("에이전트 연락처 입력: ")
    email = input("에이전트 이메일 입력: ")

    cursor.execute("INSERT INTO agents (Name, ContactNumber, Email) VALUES (%s, %s, %s)",
                   (name, contact_number, email))
    db_connection.commit()
    print("에이전트가 추가되었습니다.")

def add_client(cursor, db_connection):
    name = input("고객 이름 입력: ")
    contact_number = input("고객 연락처 입력: ")
    email = input("고객 이메일 입력: ")
    address = input("고객 주소 입력: ")

    cursor.execute("INSERT INTO clients (Name, ContactNumber, Email, Address) VALUES (%s, %s, %s, %s)",
                   (name, contact_number, email, address))
    db_connection.commit()
    print("고객이 추가되었습니다.")

def add_transaction(cursor, db_connection):
    property_id = int(input("부동산 ID 입력: "))
    client_id = int(input("고객 ID 입력: "))
    agent_id = int(input("에이전트 ID 입력: "))
    date = input("거래 날짜 입력 (YYYY-MM-DD): ")
    trans_type = input("거래 유형 입력: ")
    amount = float(input("거래 금액 입력: "))

    cursor.execute("INSERT INTO transactions (PropertyID, ClientID, AgentID, Date, Type, Amount) VALUES (%s, %s, %s, %s, %s, %s)",
                   (property_id, client_id, agent_id, date, trans_type, amount))
    db_connection.commit()
    print("거래가 추가되었습니다.")

def add_appointment(cursor, db_connection):
    client_id = int(input("고객 ID 입력: "))
    agent_id = int(input("에이전트 ID 입력: "))
    property_id = int(input("부동산 ID 입력: "))
    date = input("예약 날짜 입력 (YYYY-MM-DD): ")
    time = input("예약 시간 입력: ")

    cursor.execute("INSERT INTO appointments (ClientID, AgentID, PropertyID, Date, Time) VALUES (%s, %s, %s, %s, %s)",
                   (client_id, agent_id, property_id, date, time))
    db_connection.commit()
    print("예약이 추가되었습니다.")

if __name__ == "__main__":
    main_menu()
