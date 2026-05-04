---
layout: post
title: "🚀 智慧型紅外線 AI 冷氣控制器——我的第一步"
date: 2025-07-02 23:57:00 -0600
categories: [IoT, AI, Hardware, Project Log]
tags: [ESP32, IR, AC, Smart Home, PlatformIO, AI, Edge Computing]
---

這篇文章標誌著我開始打造一套端到端（E2E）邊緣 AI agent、用來控制冷氣的旅程。文中整理了我最初的需求，以及到目前為止已完成的基礎步驟。

## 1. 我的需求

這個專案的核心目標很清楚：

* 首先，我要做一套 **E2E 邊緣 AI agent**，能透過紅外線訊號控制分離式 **TECO** 冷氣。
* 其次，我希望同時支援 **手動智慧控制**（我設想用日後的 App 或語音介面來實作），以及會依感測器資料反應的 **自主 AI 模式**。
* 最後，我先用 **ESP32 DevKitC (WROOM)** 當第一版的 IR 橋接器，並保留未來擴充更完整後端 AI 與智慧家庭整合的空間。

## 2. 我已完成的步驟

為這個野心不小的專案打底，我已把必要的設定階段跑過一輪。

### ✅ 硬體準備

我一開始先挑選並採購硬體。我選了 **HX1838 紅外線接收／發射套件**，因為容易取得也好上手，而且我買了兩組當備品。主控方面我用 **ESP32 DevKitC**，看中它 Wi‑Fi 與藍牙能力，方便日後做智慧功能。為了方便試作，我也準備了 **麵包板**、一整組 **杜邦線**，以及 **5 V 1 A USB 變壓器** 加上可傳資料的 **micro‑USB 線**，供電與燒錄都用得上。

### ✅ 配線

硬體到手後，下一步是把基本線接好。我把 HX1838 紅外線接收器仔細接上：VCC 接到 ESP32 的 5 V（或 3.3 V）、GND 對 GND、OUT 接到 ESP32 的 **GPIO 5**。我也反覆檢查麵包板上的接線，確認牢固、正確，才通電。

### ✅ 開發環境

要好效率，穩定的開發環境很重要，而我這邊已經就緒。我裝好了 **VS Code** 和 **PlatformIO IDE 擴充套件**，在嵌入式開發上整合體驗很好。我在 PlatformIO 裡開了新專案，目標板選 **ESP32 Dev Module**，框架用 **Arduino**，好降低 ESP32 程式門檻。為了確認一切正常，我編譯並燒錄了一個簡單的「Blink + 序列埠輸出」 sketch。燒錄成功，終端機輸出如下：大約 **46.10 秒** 寫入 **269488 bytes**。

![Successful PlatformIO sketch upload to ESP32](/assets/images/first_upload.png)
*圖 1：PlatformIO sketch 成功燒錄到 ESP32。*

### ✅ 序列埠監看

要除錯與驗證，一定要會看裝置輸出，所以我把 **PlatformIO Serial Monitor**（VS Code 裡 🔌 插頭圖示）摸熟了。透過它我確認了 **LED 閃爍**，也看到序列埠每秒印出 “LED ON/OFF”，代表程式在跑。我也學會用 Ctrl+C 或垃圾桶圖示乾淨地關掉 Serial Monitor，避免之後 **序列埠被占用** 的惱人問題。

![LED ON/OFF Serial Output](/assets/images/led_on_off.png)
*圖 2：Serial Monitor 交替顯示 “LED ON” 與 “LED OFF”。*

## 3. 下一步計畫

我接下來要立即準備 HX1838 的 **IR 測試流程**，包括：

1.  在 PlatformIO 專案裡 **安裝** `IRremoteESP8266` 函式庫——處理紅外線通訊少不了它。
2.  把目前的閃燈 sketch **換成** 專門做 IR 接收／重播的 sketch。
3.  用 Serial Monitor **錄下 TECO 遙控器的代碼**，再把代碼 **重播回冷氣**，確認真的能控制。
