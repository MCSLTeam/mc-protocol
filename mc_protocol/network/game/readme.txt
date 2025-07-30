1. 游戏阶段数据包分类
游戏阶段的数据包可分为以下几类：

类别	主要包示例	方向
玩家动作	Player Position, Player Digging	Client → Server
世界同步	Chunk Data, Spawn Entity	Server → Client
物品交互	Set Slot, Window Click	双向
实体控制	Entity Metadata, Entity Velocity	Server → Client
聊天/命令	Chat Message, Command Suggestions	双向
2. 核心数据包结构详解
(1) 玩家位置更新 (Player Position & Look, 0x15) ***********************完成
客户端 → 服务器，通知服务器玩家移动和视角变化。

python
# 字段结构
X: Double (8字节)       # 坐标X
Y: Double (8字节)       # 坐标Y
Z: Double (8字节)       # 坐标Z
Yaw: Float (4字节)      # 水平视角（-180~180）
Pitch: Float (4字节)    # 垂直视角（-90~90）
On Ground: Boolean (1字节)  # 是否在地面
Teleport ID: VarInt     # 服务器用于验证的ID
示例字节流（坐标 (0,64,0)，视角 (90°,0°)，在地面）：

text
15 00 00 00 00 00 00 00 00 40 50 00 00 00 00 00 00 00 00 00 00 00 00 42 B4 00 00 00 00 00 00 01 00
(2) 挖掘方块 (Player Digging, 0x1C) *******************************完成
客户端 → 服务器，通知方块挖掘状态。

python
Status: VarInt          # 0=开始, 1=取消, 2=完成
Position: Long (8字节)  # 方块坐标 (XZY压缩)
Face: Byte              # 挖掘面 (0~5)
坐标压缩规则：

python
Position = ((X & 0x3FFFFFF) << 38) | ((Z & 0x3FFFFFF) << 12) | (Y & 0xFFF)
(3) 区块数据 (Chunk Data, 0x25)
服务器 → 客户端，发送区块地形和方块数据。

python
Chunk X: Int            # 区块X坐标
Chunk Z: Int            # 区块Z坐标
Heightmaps: NBT         # 高度图数据
Block Entities: NBT     # 方块实体数据
Data: Byte Array        # 方块和光照数据
(4) 生成实体 (Spawn Entity, 0x03)
服务器 → 客户端，生成新实体（如生物、掉落物）。

python
Entity ID: VarInt       # 实体唯一ID
UUID: UUID (16字节)     # 实体UUID
Type: VarInt            # 实体类型ID
X/Y/Z: Double           # 坐标
Pitch/Yaw: Byte         # 视角（-180~180映射到-128~127）
Velocity: Short[3]      # 速度（每个轴乘以8000）
(5) 物品栏操作 (Set Slot, 0x16)
服务器 → 客户端，更新物品栏槽位。

python
Window ID: Byte         # 0=玩家物品栏
Slot: Short             # 槽位索引
Slot Data: NBT          # 物品数据（含ID、数量、NBT标签）
3. 数据包交互流程示例
场景：玩家移动并挖掘方块

客户端 → 服务器

发送 Player Position & Look (0x15) 更新坐标。

发送 Player Digging (0x1C) 开始挖掘方块。

服务器 → 客户端

回复 Acknowledge Block Change (0x07) 确认方块更新。

广播 Block Update (0x0B) 给其他玩家。

4. 协议版本差异
不同 Minecraft 版本的包ID和结构可能不同：

1.12.2：Player Position 包ID是 0x0D，无 Teleport ID 字段。

1.18+：区块数据格式简化，移除 BitMask 改用 Data 直接存储。

5. 调试与抓包工具
Wireshark + MCProtocolLib 插件：分析原始字节流。

ViaVersion：跨版本协议转换工具。

官方协议文档：wiki.vg

6. 总结表
包类型	包ID	关键字段	方向
Player Position & Look	0x15	X/Y/Z, Yaw/Pitch, On Ground	Client → Server
Player Digging	0x1C	Status, Position, Face	Client → Server
Chunk Data	0x25	Chunk X/Z, Heightmaps, Data	Server → Client
Spawn Entity	0x03	Entity ID, Type, X/Y/Z	Server → Client
Set Slot	0x16	Window ID, Slot, Item Data	Server → Client
