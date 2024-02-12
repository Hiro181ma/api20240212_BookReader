import streamlit as st
import spacy
import re
import requests
from zipfile import ZipFile
import io

# 取り急ぎBookReaderのみの機能に絞って公開

# Pre
def remove_brackets(text):
    # 《》で囲まれた部分を取り除く正規表現パターン
    pattern = r'《[^《》]+》'
    # 正規表現を使って《》で囲まれた部分を削除
    clean_text = re.sub(pattern, '', text)
    # []で囲まれた部分を取り除く正規表現パターン
    pattern = r'［[^［］]+］'
    # 正規表現を使って[]で囲まれた部分を削除
    clean_text = re.sub(pattern, '', clean_text)
    # []で囲まれた部分を取り除く正規表現パターン
    pattern = r'［[^〔〕]+］'
    # 正規表現を使って[]で囲まれた部分を削除
    clean_text = re.sub(pattern, '', clean_text)
    return clean_text

book_dic = {
    '夏目漱石「こころ」':'https://www.aozora.gr.jp/cards/000148/files/773_ruby_5968.zip',
    '夏目漱石「坊ちゃん」':'https://www.aozora.gr.jp/cards/000148/files/752_ruby_2438.zip',
    '芥川 竜之介「羅生門」':'https://www.aozora.gr.jp/cards/000879/files/127_ruby_150.zip',
    '宮沢 賢治「銀河鉄道の夜」':'https://www.aozora.gr.jp/cards/000081/files/48222_ruby_59603.zip'
}

# Input
st.title('青空文庫の本')
st.sidebar.text('青空文庫の本')
selected_book = st.sidebar.selectbox('作品の選択：',book_dic.keys())
if selected_book: 
  url = book_dic[selected_book]  # 選択された本のURL
  response = requests.get(url)
  zip_data = response.content
  with ZipFile(io.BytesIO(zip_data), 'r') as zip_file:
    # ZIPファイル内のテキストファイルのリストを取得
    file_list = zip_file.namelist()
    # テキストファイルを開いて内容を表示
    for file_name in file_list:
        if file_name.endswith('.txt'):
            with zip_file.open(file_name) as f:
                uploaded_file = f.read().decode('shift-jis')

# Process
  if uploaded_file:
    lines = uploaded_file.split('\n')[:2]
    st.text('作家: ' + lines[1])
    st.text('作品名：' + lines[0])
    text = remove_brackets(uploaded_file)
    start_moji = text.find('----------------------',100,300)
    text = text[start_moji:]
    st.text(f'文字数：{len(text)}文字')
    st.text('これから表示します。約30秒かかります。')
    col = st.button('実行しますか？')
    if col:
      MAX_LENGTH = 50  # 1行の最大長さ
      chunks = []
      for line in text.split('\n'):
        for i in range(0, len(line), MAX_LENGTH):
          chunks.append(line[i:i+MAX_LENGTH])
      for chunk in chunks:
        st.text(chunk)
