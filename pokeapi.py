import requests
import os


# クラス定義 コンストラクタのみ
# self.でクラスが持っているフィールドが用意されるので、変数宣言がいらない
# このクラスを使用すると日本語名、英語名、高さ、重さ、フレーバーテキスト、画像を格納できる
class Pokemon:
    def __init__(
        self, ja_name="", en_name="", weight=0.0, height=0.0, flavor_text="", img=None
    ):
        self.ja_name = ja_name
        self.en_name = en_name
        self.weight = weight
        self.height = height
        self.flavor_text = flavor_text
        self.img = img


# 関数定義
# PokeApiからポケモンデータ取得
# 図鑑番号を渡すと、そのデータをPOKEAPIからとってくる
def get_pokemon(id):

    # 最後にreturnする、Pokemonクラスのインスタンス生成
    pokemon = Pokemon()

    # PokeApiにリクエスト、レスポンスをjson形式で受け取る
    # リクエスト先のURL
    response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{id}")
    # レスポンスとして受け取ったデータを、識別できるようにjson形式メソッドで作る
    # JSON形式だとディクショナリの仕様で扱える
    pokeapi = response.json()
    
    #jsonデータをキーを指定している。
    """"
    species": {
        "name": "bulbasaur",
        "url": "https://pokeapi.co/api/v2/pokemon-species/1/"
        },
        #こちらのURLに英語以外の言語データがある。
    """
    species_url = pokeapi["species"]["url"]
    #日本語データが欲しいので別のリクエストも送る
    response = requests.get(species_url)
    pokeapi_species = response.json()


    #必要なJSONデータはそろったのでその中から必要なものを取得していく。
    # 各種データをレスポンスから取得
    # 英語名、重さ、高さ、画像URL取得
    #　nameキーで取得
    pokemon.en_name = pokeapi["name"]
    #メートルとキログラムに換算するために単位を合わせるために10で割る
    pokemon.weight = float(pokeapi["weight"]) / 10
    pokemon.height = float(pokeapi["height"]) / 10
    pokemon.img = pokeapi["sprites"]["other"]["official-artwork"]["front_default"]
    """
    "sprites": {
            "back_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/back/1.png",
            "back_female": null,
            "back_shiny": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/back/shiny/1.png",
            "back_shiny_female": null,
            "front_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/1.png",
            "front_female": null,
            "front_shiny": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/shiny/1.png",
            "front_shiny_female": null,
            "other": {
            "dream_world": {
            "front_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/dream-world/1.svg",
            "front_female": null
        },
        "home": {
            "front_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/home/1.png",
            "front_female": null,
            "front_shiny": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/home/shiny/1.png",
            "front_shiny_female": null
        },
        "official-artwork": {
            "front_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/1.png",
            "front_shiny": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/shiny/1.png"
        }
        },
"""


    # 日本語の名前取得
    # for文で日本語のみの情報を絞り込む

    names = pokeapi_species["names"]
    for name in names:
        #laungageのnameがjaのものだったら、そのテキストを取得する。
        if name["language"]["name"] == "ja":
            pokemon.ja_name = name["name"]
            break

    # 日本語のフレーバーテキスト取得
    flavor_text_entries = pokeapi_species["flavor_text_entries"]
    for text in flavor_text_entries:
        #laungageのnameがjaのものだったら、そのテキストを取得する。
        if text["language"]["name"] == "ja":
            pokemon.flavor_text = text["flavor_text"]
            break
    # 画像をダウンロード、インスタンスのimg属性をダウンロードした画像ファイルのパスに変更
    download_img(pokemon)
    return pokemon


# 画像のパスを取得、インスタンスに設定
# 型アノテーションでpokemonクラスのオブジェクトを指定
def download_img(pokemon: Pokemon):
    # 同じファイル名があるか確認、無ければPokeApiから画像ダウンロード
    # 現在のpokeapi.pyがおいているフォルダ、ディレクトリを取得している
    # osモジュールのpath.dirname を実行 フォルダの絶対パスを取得する
    # c:uses\.....
    # __file__は実行しているpy.ファイルのパスを取得
    # dirnameでフォルダ名までの絶対パスを取得したい、__file__は.pyまでの絶対パス
    current_dir = os.path.dirname(__file__)
    img_path = f"{current_dir}/img/{pokemon.en_name}.png"
    # 文字列で。最終的にはこういう名前で、このパスに保存しますよという文字列
    # .pyの実行フォルダ内の、imgフォルダに、ぽけ英語名.png

    # 同名の画像ファイルが無ければダウンロードして保存
    # osもジュールの、path isfileで、パスが存在しているかをチェック
    if not os.path.isfile(img_path):
        #リクエストモジュールのゲットメソッドで、imgを指定、
        # .contentだとバイナリデータでデータを取得できる
        image = requests.get(pokemon.img).content
        # openこの場所に保存しますよ、バイナリを書き込み保存はwbモードで
        # 開いたファイルをfとして扱う fileとかでもいい
        with open(img_path, "wb") as f:
            f.write(image)#取得したバイナリデータを、open.writeで書き出す
        #with句は終わったときに ファイルオブジェクトを閉じる 
        # open クラスで帰ってくるバッファードライターのwriteメソッドで書き出す
        # openブロック内でwriteを実行している
    else:
        print("既にダウンロード済みのポケモン画像です")

    # ローカルの画像パスを設定
    pokemon.img = img_path













