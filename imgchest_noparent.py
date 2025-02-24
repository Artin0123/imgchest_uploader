import os
import requests
import sys
from plyer import notification

# 將您的 API 金鑰替換為實際的金鑰
API_KEY = "QmkurCKSVnMx26QkKadAuMAZU8LGGm1XcSzqVMOE6ece33f3"


def upload_images_to_imagechest(
    image_paths, title=None, privacy="hidden", anonymous=False, nsfw=False
):
    url = "https://api.imgchest.com/v1/post"

    # 修改：直接使用布林值
    data = {}
    if title:  # 只有當標題存在時才加入
        data["title"] = title
    if privacy != "hidden":  # 只有當隱私設定不是預設值時才加入
        data["privacy"] = privacy
    if anonymous:  # 只有當要求匿名時才加入
        data["anonymous"] = "true"
    if nsfw:  # 只有當內容為 NSFW 時才加入
        data["nsfw"] = "true"

    # 5. images[] (保持在 files 參數中)
    files = [("images[]", open(path, "rb")) for path in image_paths]

    headers = {"Authorization": f"Bearer {API_KEY}", "Accept": "application/json"}

    # 新增更多偵錯資訊
    print("正在發送的資料：")
    # print(f"Headers: {headers}")
    print(f"Data: {data}")

    try:
        response = requests.post(url, files=files, data=data, headers=headers)
        if response.status_code == 200:
            result = response.json()
            print("上傳成功！")
            # 顯示更詳細的上傳結果
            if "data" in result:
                print(f"上傳ID: {result['data']['id']}")
                print(f"標題: {result['data']['title']}")
                print(f"圖片數量: {result['data']['image_count']}")
                print("圖片連結:")
                for img in result["data"]["images"]:
                    print(f"- {img['link']}")
        else:
            print(f"上傳失敗，狀態碼：{response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"上傳過程發生錯誤：{str(e)}")
    finally:
        # 確保所有檔案都被正確關閉
        for _, file in files:
            file.close()


if __name__ == "__main__":
    # 獲取當前 Python 檔案的目錄路徑
    current_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    # 切換到該目錄
    os.chdir(current_dir)

    # 獲取當前目錄名稱
    folder_name = os.path.basename(current_dir)

    image_files = [
        f
        for f in os.listdir()
        if f.lower().endswith((".png", ".jpg", ".jpeg", ".webp"))
    ]
    image_paths = [os.path.join(os.getcwd(), f) for f in image_files]
    total_images = len(image_paths)
    if total_images == 0:
        print("當前路徑沒有圖片。")
        # 使用 plyer 顯示通知
        notification.notify(title="圖片上傳", message="當前路徑沒有圖片", timeout=3)
    else:
        batch_size = 20
        for i in range(0, total_images, batch_size):
            batch_images = image_paths[i : i + batch_size]
            title = f"{folder_name}_{i // batch_size + 1}"
            upload_images_to_imagechest(
                batch_images,
                title=title,
                privacy="hidden",
                anonymous=False,
                nsfw=False,
            )
            print(f"已上傳 {min(i + batch_size, total_images)} / {total_images} 張圖片")

        # 所有批次上傳完成後顯示通知
        notification.notify(
            title="圖片上傳完成", message=f"成功上傳 {total_images} 張圖片", timeout=5
        )
