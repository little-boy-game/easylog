import os 
import random
import json
import arrow
import threading  # 1. 导入线程锁模块

txt = {
    "zh":{
        "imm_init":"日志初始化完成"
    },
    "en":{
        "imm_init":"Log initialized"
    },
    "es": {
        "imm_init": "Registro inicializado"
    },
    "fr": {
        "imm_init": "Journal initialisé"
    },
    "de": {
        "imm_init": "Protokoll initialisiert"
    },
    "jp": {
        "imm_init": "ログが初期化されました"
    },
    "ru": {
        "imm_init": "Журнал инициализирован"
    },
    "it": {
        "imm_init": "Registro inizializzato"
    },
    "pt": {
        "imm_init": "Log inicializado"
    },
    "kr": {
        "imm_init": "로그가 초기화되었습니다"
    }
}

class Logger:
    def __init__(self,logname="log.log",method="imm",lang="en"):
        self.recording = []
        self.Method = method
        self.logname = logname
        self.lock = threading.Lock()  # 2. 初始化实例级锁（每个Logger独立一把锁）
        if self.Method == "imm":
            with open(self.logname,"w") as self.f:
                time = arrow.now().format("HH:mm:ss")
                self.f.write(f"[info {time}] {txt[lang]['imm_init']}\n")
        elif self.Method == "alw":
            self.f = open(self.logname,"a")
            time = arrow.now().format("HH:mm:ss")
            self.f.write(f"[info {time}] {txt[lang]['imm_init']}\n")
        elif self.Method == "beh":
            self.recording_beh = []
            time = arrow.now().format("HH:mm:ss")
            self.recording_beh.append(f"[info {time}] {txt[lang]['imm_init']}")
        else:
            raise ValueError("Method must be 'imm' or 'alw'")
    def __str__(self) :
        v = ''
        for i in self.recording:
            v += i + ','
        return v
    
    # 3. 所有写入方法添加锁保护（以info为例，其他方法逻辑一致）
    def info(self,info):
        self.recording.append(f"[info] {info}")
        self.lock.acquire()  # 获取锁（未拿到则阻塞）
        try:  # 确保异常时锁仍能释放
            time = arrow.now().format("HH:mm:ss")
            if self.Method == "imm":
                with open(self.logname,"a") as self.f:
                    self.f.write(f"[info {time}] {info}\n")
            elif self.Method == "alw":
                self.f.write(f"[info {time}] {info}\n")
            elif self.Method == "beh":
                self.recording_beh.append(f"[info {time}] {info}")
        finally:
            self.lock.release()  # 释放锁（必执行）
    
    def warning(self,info):
        self.recording.append(f"[warning] {info}")
        self.lock.acquire()
        try:
            time = arrow.now().format("HH:mm:ss")
            if self.Method == "imm":
                with open(self.logname,"a") as self.f:
                    self.f.write(f"[warning {time}] {info}\n")
            elif self.Method == "alw":
                self.f.write(f"[warning {time}] {info}\n")
            elif self.Method == "beh":
                self.recording_beh.append(f"[warning {time}] {info}")
        finally:
            self.lock.release()
    
    def error(self,info):
        self.recording.append(f"[error] {info}")
        self.lock.acquire()
        try:
            time = arrow.now().format("HH:mm:ss")
            if self.Method == "imm":
                with open(self.logname,"a") as self.f:
                    self.f.write(f"[error {time}] {info}\n")
            elif self.Method == "alw":
                self.f.write(f"[error {time}] {info}\n")
            elif self.Method == "beh":
                self.recording_beh.append(f"[error {time}] {info}")
        finally:
            self.lock.release()
    
    def debug(self,info):
        self.recording.append(f"[debug] {info}")
        self.lock.acquire()
        try:
            time = arrow.now().format("HH:mm:ss")
            if self.Method == "imm":
                with open(self.logname,"a") as self.f:
                    self.f.write(f"[debug {time}] {info}\n")
            elif self.Method == "alw":
                self.f.write(f"[debug {time}] {info}\n")
            elif self.Method == "beh":
                self.recording_beh.append(f"[debug {time}] {info}")
        finally:
            self.lock.release()
    
    def log(self,level,info):
        self.recording.append(f"[{level}] {info}")
        self.lock.acquire()
        try:
            time = arrow.now().format("HH:mm:ss")
            if self.Method == "imm":
                with open(self.logname,"a") as self.f:
                    self.f.write(f"[{level} {time}] {info}\n")
            elif self.Method == "alw":
                self.f.write(f"[{level} {time}] {info}\n")
            elif self.Method == "beh":
                self.recording_beh.append(f"[{level} {time}] {info}")
        finally:
            self.lock.release()
    
    # close方法无需加锁（仅在alw模式关闭文件，且需用户确保写入完成后调用）
    def close(self):
        if self.Method == "alw":
            self.f.close()
        else:
            Warning("close method is only available in 'alw' mode")
    def save(self):
        if self.Method == "beh":
            with open(self.logname,"w") as self.f:
                for record in self.recording_beh:
                    self.f.write(record+"\n")
        else:
            Warning("Save method is only available in 'beh' mode")