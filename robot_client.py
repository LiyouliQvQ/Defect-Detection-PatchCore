import socket
import time
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] [%(name)s] : %(message)s')
logger = logging.getLogger("RobotArm_Client")

def run_inspection_cycle(host='127.0.0.1', port=8080):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((host, port))
        logger.info("已成功接入视觉中枢，开始执行 [差速器壳体] 全方位巡检任务。")
        
        # --- 动作 1：检测法兰面 ---
        logger.info(">> 关节伺服启动，携带相机移动至 [机位 1: 外侧法兰面]...")
        time.sleep(2) 
        logger.info("已到达机位 1，姿态锁定。发送视觉触发指令: [TRIGGER_FLANGE]")
        client_socket.sendall("TRIGGER_FLANGE".encode('utf-8'))
        
        result_flange = client_socket.recv(1024).decode('utf-8')
        logger.info(f"收到机位 1 视觉反馈: {result_flange}")
        time.sleep(1) # 停顿一下，准备切机位

        # --- 动作 2：检测内部深孔 ---
        logger.info(">> 关节伺服启动，末端探入壳体，移动至 [机位 2: 内部深孔]...")
        time.sleep(2)
        logger.info("已到达机位 2，姿态锁定。发送视觉触发指令: [TRIGGER_HOLE]")
        client_socket.sendall("TRIGGER_HOLE".encode('utf-8'))
        
        result_hole = client_socket.recv(1024).decode('utf-8')
        logger.info(f"收到机位 2 视觉反馈: {result_hole}")
        
        # --- 综合判定 ---
        if "OK" in result_flange and "OK" in result_hole:
            logger.info("巡检完毕，该壳体 [全部合格]。退回安全等待区。\n" + "="*60)
        else:
            logger.warning("巡检完毕，该壳体 [存在缺陷]！亮起红灯报警并等待人工介入。\n" + "="*60)
            
    except ConnectionRefusedError:
        logger.error("无法连接视觉大脑，请检查服务端状态。")
    finally:
        client_socket.close()

if __name__ == "__main__":
    # 模拟对流水线上的 2 个壳体进行连续巡检
    for i in range(1, 3):
        logger.info(f"\n====== 传送带就位，开始检测今天第 {i} 个壳体 ======")
        run_inspection_cycle()
        time.sleep(3) # 模拟传送带把下一个零件送过来的时间