import socket
import time
import logging
import random

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s')
logger = logging.getLogger("Vision_Server")

def start_server(host='127.0.0.1', port=8080):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    logger.info(f"视觉多专家总控系统已就绪，端口 {port} 监听中...")

    while True:
        conn, addr = server_socket.accept()
        logger.info(f"机械臂客户端接入，来源 IP: {addr}")

        try:
            while True:
                data = conn.recv(1024).decode('utf-8')
                if not data:
                    break
                
                logger.info(f"收到硬件请求: [{data}]")
                
                # --- 多专家路由分发中心 ---
                if data == "TRIGGER_FLANGE":
                    logger.info("📷 海康相机(法兰焦段) 极速曝光抓图...")
                    time.sleep(0.5)
                    logger.info("🧠 唤醒 [外侧法兰面_PatchCore专家] 进行推理...")
                    time.sleep(1)
                    # 模拟 90% 的概率是良品
                    result = "[OK] 法兰面无划伤" if random.random() > 0.1 else "[NG] 检出法兰边缘划伤"
                    
                elif data == "TRIGGER_HOLE":
                    logger.info("📷 海康相机(深孔焦段) 极速曝光抓图...")
                    time.sleep(0.5)
                    logger.info("🧠 唤醒 [内部深孔_PatchCore专家] 进行推理...")
                    time.sleep(1)
                    # 模拟 80% 的概率是良品
                    result = "[OK] 深孔内壁平整" if random.random() > 0.2 else "[NG] 检出深孔内壁砂眼"
                else:
                    result = "[ERROR] 未知机位指令"

                logger.info(f"★ 推理完毕，下发判定结果: {result}\n" + "-"*40)
                conn.sendall(result.encode('utf-8'))
                    
        except ConnectionResetError:
            logger.warning("机械臂通讯中断。")
        finally:
            conn.close()

if __name__ == "__main__":
    start_server()