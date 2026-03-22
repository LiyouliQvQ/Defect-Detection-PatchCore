import socket
import time

def simulate_robot_arm():
    print("=======================================")
    print("🦾 [机械臂] 准备就绪，正在连接视觉电脑...")
    print("=======================================")
    
    # 1. 创建 TCP Socket 并连接视觉电脑
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 在真实产线，这里要填你笔记本电脑的真实局域网 IP (比如 192.168.1.100)
    client.connect(('127.0.0.1', 8080)) 
    print("✅ [机械臂] 成功连上视觉系统！\n")

    # 模拟产线动作：抓取 -> 移动 -> 拍照 -> 丢弃
    print("🦾 [机械臂] 正在抓取差速器壳体...")
    time.sleep(1.5) # 模拟机械臂运动时间
    print("🦾 [机械臂] 已移动到相机正下方 (拍照位 1)！")
    
    # 2. 发送拍照指令
    cmd = "SNAP_POS_1"
    print(f"📤 [机械臂] 向视觉系统发送指令: {cmd}")
    client.sendall(cmd.encode('utf-8'))

    # 3. 停在原地，死等视觉系统返回结果
    print("⏳ [机械臂] 悬停等待 AI 判定结果...")
    result = client.recv(1024).decode('utf-8')
    print(f"📥 [机械臂] 收到视觉判定结果: {result}")

    # 4. 根据 AI 结果决定把壳体放哪
    if result == "OK":
        print("🦾 [机械臂] 结果为良品，将其平稳放入【合格品传送带】。")
    elif result == "NG_DEFECT":
        print("🦾 [机械臂] 警告！发现次品，将其丢入【红色废料筐】！")

    # 5. 动作完成，断开连接
    time.sleep(1)
    print("\n🛑 [机械臂] 演示结束，断开通讯。")
    client.sendall("QUIT".encode('utf-8'))
    client.close()

if __name__ == '__main__':
    simulate_robot_arm()