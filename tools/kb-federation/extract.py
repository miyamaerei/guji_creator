"""extract.py —— E 阶段：调 adapter 抽出标准中间表

extract_book(book_id) -> {layer_key: LayerSlice}
"""

from adapters import make_adapter


def extract_book(book_id):
    return make_adapter(book_id).discover()
