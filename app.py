import cv2
import numpy as np
import tkinter as tk

from tkinterdnd2 import TkinterDnD, DND_FILES
from tkinter import Frame, filedialog, messagebox


def conversion(path):

    # 画像読み込み
    if path == "":
        raise ValueError(f"ファイルが選択されていません。")
    photo = cv2.imread(path)
    # 保存先
    list_path = path.split("/")
    list_path[-1] = "conversion_" + list_path[-1]
    save_path = "/".join(list_path)

    # 画像サイズ取得
    height, width = photo.shape[:2]

    # 調整後のサイズ指定
    if height < width:
        size = width, width
    else:
        size = height, height

    # 背景の処理
    base_photo = np.ones((size[1], size[0], 3), np.uint8) * 255

    # スケーリングファクターを計算
    ash = size[1] / height

    asw = size[0] / width

    # アスペクト比を保持するためのサイズ計算
    if asw < ash:
        sizeas = (int(width * asw), int(height * asw))
    else:
        sizeas = (int(width * ash), int(height * ash))

    # リサイズ
    photo = cv2.resize(photo, dsize=sizeas)

    # 合成
    base_photo[
        int(size[1] / 2 - sizeas[1] / 2) : int(size[1] / 2 + sizeas[1] / 2),
        int(size[0] / 2 - sizeas[0] / 2) : int(size[0] / 2 + sizeas[0] / 2),
        :,
    ] = photo

    # 保存
    cv2.imwrite(save_path, base_photo)

    return True


class Application(Frame):
    def __init__(self, root):
        super().__init__(root, width=520, height=420, borderwidth=4, relief="groove")
        self.pack()
        self.pack_propagate(0)
        self.root = root
        self.create_widgets()

    def add_listbox(self, event):
        if isinstance(event, str):
            file_path = event
        else:
            file_path = event.data.replace("\\", "/").replace("{", "").replace("}", "")

        self.path = file_path
        # print(self.path)
        self.path_label["text"] = f"指定したパス\n{self.path}"

    def choose_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg;*.jpeg;*.png")]
        )
        if file_path:
            self.path = file_path
            self.add_listbox(file_path)

    def submit(self):
        if hasattr(self, "path"):
            try:
                if conversion(self.path):
                    messagebox.showinfo("成功", "変換が完了しました！")
                self.path = ""
                self.path_label["text"] = ""

            except Exception as e:
                messagebox.showerror("エラー", f"変換中にエラーが発生しました: {e}")
        else:
            messagebox.showerror("エラー", "ファイルが選択されていません。")

    def create_widgets(self):
        # ドロップウィジェット
        self.frame = tk.Frame(self.master)
        self.listbox = tk.Listbox(self.frame, width=76, height=15, selectmode=tk.SINGLE)
        self.listbox.drop_target_register(DND_FILES)
        self.listbox.dnd_bind("<<Drop>>", self.add_listbox)
        self.frame.place(x=20, y=20)
        self.listbox.pack(fill=tk.X, side=tk.LEFT)

        # Listboxの中心にテキストを配置するためのLabelを作成
        self.text_label = tk.Label(
            self.frame, text="ここにドロップ！", bg="white", highlightbackground="white"
        )
        self.text_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # ファイル選択ボタン
        choose_file_btn = tk.Button(self, text="ファイル選択", command=self.choose_file)
        choose_file_btn.place(x=300, y=350, width=80, height=30)

        # 指定したパスを表示
        self.path_label = tk.Label(text=" ")
        self.path_label.place(x=250, y=300, anchor="center")

        # 実行ボタン
        submit_btn = tk.Button(self, text="実行", command=self.submit)
        submit_btn.place(x=400, y=350, width=80, height=30)


root = TkinterDnD.Tk()
root = root
root.title("photo_conversion")
root.geometry("500x400")
root.resizable(False, False)

app = Application(root)
app.mainloop()  # アプリケーションの起動
