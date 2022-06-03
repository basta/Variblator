from css.base import BaseCSS


class TextInputCSS(BaseCSS):
    def get_data(self) -> bytes:
        return b"""
            #text_input {
                background-color: #000000;
                color: #ffffff;
            }
        """
