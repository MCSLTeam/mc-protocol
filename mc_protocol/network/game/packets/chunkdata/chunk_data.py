# accept:区块更新
from nbt import nbt
from io import BytesIO
from struct import unpack
from packet import PacketAccept
from packet import PACK_IDS
from packet.varint_processor import VarIntProcessor

class ChunkData(PacketAccept):
    def __init__(self, data: bytes, hasSkyLight: bool, version: int):
        super().__init__(PACK_IDS["game"]["chunkData"], data)
        self.hasSkyLight = hasSkyLight
        self.version = version # 协议号

    # 利用Buffer缓冲区来读取varint,郝处:能动态更新buffer指针的值
    def readVarintFromBuffer(buffer: BytesIO):
        sum = 0
        shift = 0
        while True:
            byte = buffer.read(1) 
            sum |= (byte & 0b01111111) << shift
            shift += 7
            if (byte | 0b10000000) == 0:
                return sum
            

    def getMsg(self):
        flag = 0

        # 拿到字段
        chunkX = bytearray()
        chunkZ = bytearray()
        lastField = bytearray()
        for byte in self.data:
            if not flag == 0 and byte == self.id:
                return "Error: Wrong pack id"
            if flag >= 1 and flag <= 4:
                chunkX.append(byte)
            if flag >= 5 and flag <= 8:
                chunkZ.append(byte)
            if flag >= 9:
                lastField.append(byte)
            flag += 1

        # 拿到chunkx,z的值，这里用了int.from_bytes,他接受一个4字节的字节流,"big"代表大端序
        chunkX = int.from_bytes(bytes(chunkX), "big")
        chunkZ = int.from_bytes(bytes(chunkZ), "big")

        # 傻逼mc不给我height_map的长度，只能动态解析
        lastField = bytes(lastField)

        # NBTFile 方法可以帮我们从字节缓冲区里面动态的解析出nbt
        lastFieldBuffer = BytesIO(lastField)
        heightMap = nbt.NBTFile(buffer=lastFieldBuffer)

        # 开始解析Data
        length, offset = VarIntProcessor.readVarInt(lastFieldBuffer.read(1)) # 拿到Data的总长度
        Data = [] # data 由多个section组成,每个section包含一组16*16*16的方块（共4096个）
        for pointer in range(length):
            paletteType = lastFieldBuffer.read(1)[0] # 拿到调色板类型（0代表全局id, 1,2……就代表调色板)
            blockState = dict() # 方块状态
            if paletteType == 0:
                blockIDS = [] # 读取全局方块的id
                for pointer in range(4096):
                    blockIDS.append(int.from_bytes(lastFieldBuffer.read(2))) # 每个方块id两个字节
                blockState = {
                    "type": "direct",
                    "data": blockIDS
                }
            else: # 调色板优化
                paletteSize = self.readVarintFromBuffer(lastFieldBuffer) #获得调色板大小
                palette = [] # 拿到调色板
                for pointer in range(paletteSize):
                    # 拿到所有调色盘id
                    palette.append(self.readVarintFromBuffer(lastFieldBuffer))
                # 处理bits_per_block的山(每个方块所占有的位数)
                bits_per_block = max(4, (paletteSize - 1).bit_length()) # mc强制要求他至少是4,原因是兼容问题，和对齐处理更高效什么乱七八糟的

                # 接下来就是把这个索引对应的数组给他解码出来
                blocks = [] 
                neededBites = bits_per_block * 4096 # 计算数组所需的位数
                neededBytes = (neededBites + 7) // 8  # 加7再向下取整：向上取整 防止数据丢失 这样就可以计算得到数组所需的字节数
                data = lastFieldBuffer.read(neededBytes) # 把这一块先读下来
                for pointer in range(4096): # 开始逐位读取
                    sum = 0
                    bit_offset = pointer * bits_per_block # 起始位置
                    for subPointer in range(bits_per_block): # 逐位读取
                        byte_pos = (bit_offset + subPointer) // 8 # 获得字节索引
                        bit_pos = (bit_offset + subPointer) % 8 # 位数索引
                        # 上面那两个东西简单来说就是解析进行了几个字节零几位

                        if byte_pos < len(data):
                            bit = (data[byte_pos] >> bit_pos) & 1 # 先提取一位，再拼接到sum里
                            sum |= bit << subPointer
                    blocks.append(sum)
                blockState = {
                    "type": "palette",
                    "palette": palette,
                    "indices": blocks
                }
            
            #方块照明
            blockLight = lastFieldBuffer.read(2048)

            #天空关照
            skyLight = lastFieldBuffer.read(2048) if self.hasSkyLight else None
            Data.append({
                "block_states": blockState,
                "block_light": blockLight,
                "sky_light": skyLight
            })

        # 拿到方块实体数据
        blockEntitiesC = self.readVarintFromBuffer(lastFieldBuffer) # 拿到方块实体的数量
        blockEntities = []
        for pointer in range(blockEntitiesC):
            # 拿到表示坐标的代码(8字节长整型)
            posCode = unpack(">Q",lastFieldBuffer.read(8))[0] # unpack 返回一个包含长整型数字的元组，只有一个元素
            x = posCode >> 38 # 还是大端序
            y = posCode & 0xfff
            z = (posCode >> 12) & 0x3ffffff # 26位掩码可以只保留有效位

            # 处理一下y的符号，那个傻逼数据包y只存12位，所以说得给他手动加一下符号
            if (y & 0x800) != 0:
                y |= 0xfffff000

            blockTypeID = self.readVarintFromBuffer(lastFieldBuffer) # 方块id
            nbtLength = self.readVarintFromBuffer(lastFieldBuffer) # nbt长度
            nbtData = nbt.NBTFile(lastFieldBuffer.read(nbtLength)) # 获得nbt
            blockEntities.append({
                "position": {
                    "x": x,
                    "y": y,
                    "z": z
                },
                "type_id": blockTypeID,
                "nbt_data": nbtData
            })

        return {
            "chunk_pos": {
                "chunk_x": chunkX,
                "chunk_z": chunkZ,  
            },
            "height_map": heightMap,
            "Data": Data,
            "block_entities": blockEntities
        }





                

                

        
