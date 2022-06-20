from css.base import BaseCSS


class TextInputCSS(BaseCSS):
    def get_data(self) -> bytes:
        return b"""
            * {
                background-color: #000000;
                color: #ffffff;
                font-size: 16px;
                padding: 5px;
                line-height: 32px;
            }
        """


class TextOutputCSS(BaseCSS):
    def get_data(self) -> bytes:
        return b"""
            * {
                font-size: 16px;
                padding-left: 10px;
                line-height: 32px;
            }
        """
