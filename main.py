import tkinter as tk
import pokeapi


# ボタンクリック時に実行する関数
def change_data(entry_id):
    #pokeapiからデータを取得
    pokemon = pokeapi.get_pokemon(entry_id)
    #ネームラベルを作る
    name_label["text"] = pokemon.ja_name
    #高さと重さのラベルを作る
    data_label["text"] = f"高さ:{pokemon.height}m,重さ:{pokemon.weight}kg"
    #画像ファイルでイメージを作る
    img["file"] = pokemon.img
    flavor_text_msg["text"] = pokemon.flavor_text

#下記のデータを書くおぬして、代入しなおしている


"""
#print(__name__)をコンソールで出すと__main__と出る。
pokeAPIの方で、print(__name__)これを実行すると、mainになる。

モジュール名が出てくる
実行したファイル。__main__
インポートしたファイルの中はモジュールの名前がnameで出てくる。
実行ファイルか、インポートされたファイルかを区別できるもの

main.pyを実行したときにだけ実行されるのがpokeapi。
importはコードの中身が丸々書いてあるのと同じ意味。


"""

if __name__ == "__main__":
    font_size = 20 # ウィンドウ上の文字サイズ
    pokemon = pokeapi.get_pokemon(1) #最初のポケモンデータを取得しておく

    # ウィンドウ作成
    root = tk.Tk()
    root.geometry("1280x720")

    # フレーム用意、配置
    #フレームが２つある。入力欄と、データ欄。その中にパーツが入っている。
    #divタグのようなもの。
    entry_frame = tk.Frame(root)  # 入力欄フレーム
    pokemon_frame = tk.Frame(root)  # ポケモンデータ表示フレーム
    entry_frame.pack()
    pokemon_frame.pack()

    # 図鑑番号入力欄用のウィジェット用意
    #　今回はrootではなくフレームに作ったものを配置している
    # Label Entry Button　は作った段階では配置されていない
    entry_label = tk.Label(entry_frame, text="図鑑番号:", font=font_size)
    #entryで入力内容をとる
    entry_id = tk.Entry(entry_frame,font=font_size)
    #検索ボタンをつくる ボタンが押されたとき change_data実行(入力内容)
    #ラムダ式、エントリーidのゲットは入力欄の内容を取得する
    entry_button = tk.Button(
        entry_frame, text="検索", command=lambda: change_data(entry_id.get())
    )

    # ウィジェット配置 
    # LabelとEntryとButtonを、gridで等間隔配置
    #　packではそれができないため　row 縦の列 col横の列
    entry_label.grid(row=0, column=0)
    entry_id.grid(row=0, column=1)
    entry_button.grid(row=0, column=2)

    # ポケモンデータ表示用のウィジェット用意
    name_label = tk.Label(pokemon_frame, text=pokemon.ja_name, font=font_size)
    #フォトイメージでイメージを格納 
    img = tk.PhotoImage(file=pokemon.img)
    image_label = tk.Label(pokemon_frame, image=img)
    #ラベルで描画する
    data_label = tk.Label(
        pokemon_frame,
        text=f"高さ:{pokemon.height}m,重さ:{pokemon.weight}kg",
        font=font_size,
    )

    #Labelではなくメッセージで文章を出している
    #複数行であるため  引数は、場所、テキスト内容、フォント、表示範囲
    #引数の名前をキーになると再代入される
    flavor_text_msg = tk.Message(
        pokemon_frame,
        text=pokemon.flavor_text,
        font=font_size,
        width=400,
    )

    # ウィジェット配置
    #パックであるため、個の順番で表示される
    name_label.pack()
    image_label.pack()
    data_label.pack()
    flavor_text_msg.pack(pady=(10, 0))



    
    #イベントには仮引数が絶対必要
    #関数を指定することで、ボタンを押したらこういう動きをするとまとめる
    def key(e):
        print(e.keysym)
    def mouse(e):
        print(e.x)
    


    #キー入力やどこかクリックすると、値が表示される
    #仮引数のeにイベント引数に入る
    #e.keysymでどの入力があったか取得できる
    #e.xでｘ座標を取得できる 
    root.bind("<Key>",key)
    root.bind("<Button-1>",mouse)
    #Butoon-2 右クリック、3ならばマウスホイールクリック
    #KeyRelearse Keyキーを離したとき
    #motionはマウスの移動を検出
    #tkinter イベント検出で情報がわかる
    #root = ウィンドウそのもの 
    # ルートの部分をtkinterのパーツを指定すれば
    # 特定の場所ラベルの場所をクリックしたときなど、テキストをボタン化もできる





	# メインループ
    # tkインターはウィンドウ出して消してを高速で繰り返しているためループがいる
    root.mainloop()