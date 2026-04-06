import socketio
import time
import threading

# Socket.IO 클라이언트
sio = socketio.Client()

@sio.event
def connect():
    print("✅ [GPIO] Node.js 서버에 연결 성공!")

@sio.event
def disconnect():
    print("❌ [GPIO] 연결이 끊어졌습니다.")

# GPIO 입력 시뮬레이션
# user_input 부분을 GPIO 입력으로 변경해서 진행하면 됨.
def gpio_input_simulator():
    print("\n🔧 [GPIO] 입력 시뮬레이션 시작")
    print("   → 콘솔에 'i' 입력하고 Enter 누르면 GPIO 입력 발생!")
    print("   → 실제 Pi에서는 버튼/센서로 자동 감지됩니다.\n")
    
    while True:
        user_input = input().strip().lower()
        if user_input == 'i':
            sio.emit('gpio_input', {
                'status': 'triggered',
                'message': '🚨화재 경보🚨',
                'time': time.strftime('%H:%M:%S')
            })
            print(f"🚨 [GPIO] 입력 발생 → Node.js로 알람 전송! ({time.strftime('%H:%M:%S')})")

if __name__ == "__main__":
    try:
        sio.connect('http://localhost:3000')
        
        # 입력 감지 스레드 시작
        threading.Thread(target=gpio_input_simulator, daemon=True).start()
        
        sio.wait()
        
    except Exception as e:
        print("❌ [GPIO] 연결 실패:", e)
