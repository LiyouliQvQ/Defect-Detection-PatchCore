import os
import socket
import time
import shutil  # 🌟 新增：用于复制和保存次品照片

# ==========================================
# 🤫 核武器级静音模式：彻底封死底层框架的嘴巴
# ==========================================
import logging
import warnings
warnings.filterwarnings("ignore")
# 🌟 精准狙击 PyTorch Lightning 的核心播报员
logging.getLogger("pytorch_lightning.utilities.rank_zero").setLevel(logging.ERROR)
logging.getLogger("pytorch_lightning.accelerators.cuda").setLevel(logging.ERROR)
logging.getLogger("pytorch_lightning").setLevel(logging.ERROR)
logging.getLogger("anomalib").setLevel(logging.ERROR)

import torch
torch.set_float32_matmul_precision('medium')

from anomalib.engine import Engine
from anomalib.models import Patchcore
from anomalib.data import PredictDataset

# ==========================================
# 1. 路径与黑匣子配置
# ==========================================
WEIGHT_PATH = "./results/Patchcore/differential_housing/latest/weights/lightning/model.ckpt"
# 注意：这里换成你想测试的图片路径 (根据你截图，你目前测试的是 goodtest_01.png)
TEST_IMAGE_PATH = "datasets/differential_housing/test/good/goodtest_02.png"

# 🌟 自动创建“次品黑匣子”文件夹
RECORDS_DIR = "./bad_records"
if not os.path.exists(RECORDS_DIR):
    os.makedirs(RECORDS_DIR)

def start_real_ai_server():
    print("=======================================")
    print("⏳ [视觉系统] 正在静默挂载 PatchCore AI 大脑...")
    
    model = Patchcore(backbone="wide_resnet50_2", layers=["layer2", "layer3"])
    engine = Engine(enable_progress_bar=False) 
    
    dataset = PredictDataset(path=TEST_IMAGE_PATH, image_size=(256, 256))
    
    print("✅ [视觉系统] 大脑准备完毕，随时可以推理！")
    print("=======================================")

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('127.0.0.1', 8080)) 
    server.listen(1)
    
    print("👁️ [视觉系统] 正在端口 8080 监听机械臂信号...")

    conn, addr = server.accept()
    print(f"✅ [视觉系统] 艾力特机械臂已连接！")

    while True:
        data = conn.recv(1024).decode('utf-8')
        if not data:
            break 
            
        print(f"\n📥 [视觉系统] 收到机械臂指令: {data}")
        
        if data == "SNAP_POS_1":
            print("📸 [视觉系统] 触发拍照 -> 正在读取并分析测试照片...")
            
            start_time = time.time()
            predictions = engine.predict(model=model, ckpt_path=WEIGHT_PATH, dataset=dataset)
            cost_time = time.time() - start_time
            
            batch_result = predictions[0]
            is_defective = bool(batch_result.pred_label.item())
            score = float(batch_result.pred_score.item())
            
            # ==========================================
            # 🌟 核心判定与黑匣子存档逻辑
            # ==========================================
            if is_defective:
                ai_result = "NG_DEFECT"
                
                # 记录时间戳 (格式：年月日_时分秒)
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                # 拼接存档文件名
                save_name = f"NG_{timestamp}_score{score:.2f}.png"
                save_path = os.path.join(RECORDS_DIR, save_name)
                
                # 把当前的次品照片悄悄复制到黑匣子里留作证据
                shutil.copy(TEST_IMAGE_PATH, save_path)
                
                print(f"🚨 [视觉系统] 判定: 次品 (得分: {score:.2f}, 耗时: {cost_time:.3f}秒)")
                print(f"📁 [黑匣子] 已将次品照片存档为: {save_name}")
            else:
                ai_result = "OK"
                print(f"🟢 [视觉系统] 判定: 良品 (得分: {score:.2f}, 耗时: {cost_time:.3f}秒)")
            
            print(f"📤 [视觉系统] 将真实判定结果发给机械臂: {ai_result}")
            conn.sendall(ai_result.encode('utf-8'))
            
        elif data == "QUIT":
            print("🛑 [视觉系统] 收到停机指令，关闭服务器。")
            break

    conn.close()
    server.close()

if __name__ == '__main__':
    start_real_ai_server()