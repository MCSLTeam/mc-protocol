
PACK_IDS = {
    C2SLoginStartPacket: 0x00,
    C2SEncryptionResponse: 0x01,
    S2CEncryptionRequest: 0x01,
    "game": { # 游戏
        "playerPosition": b"\x18",
        "playerPosAndLook": b"\x15",
        "playerDigging": b"\x1c",
        "playerBlockPlacement": b"\x2f",
        "useItem": b"\x32",
        "interactEntity": b"\x31", # 攻击实体
        "chunkData": b"\x25" # 区块更新
    }
}