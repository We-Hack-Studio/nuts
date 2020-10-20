#!/usr/bin/env python

"""
Taking from https://github.com/maethor/avatar-generator.
"""

import os
from io import BytesIO
from random import randint, seed

from PIL import Image, ImageDraw, ImageFont

__all__ = ["AvatarGenerator"]


class AvatarGenerator:
    FONT_COLOR = (255, 255, 255)
    MIN_RENDER_SIZE = 100

    @classmethod
    def generate(cls, string, size=100, filetype="PNG"):
        """
        Generates a squared avatar with random background color.
        :param size: size of the avatar, in pixels
        :param string: string to be used to print text and seed the random
        :param filetype: the file format of the image (i.e. JPEG, PNG)
        """
        render_size = max(size, cls.MIN_RENDER_SIZE)
        image = Image.new(
            "RGB", (render_size, render_size), cls._background_color(string)
        )
        draw = ImageDraw.Draw(image)
        font = cls._font(render_size)
        text = cls._text(string)
        draw.text(
            cls._text_position(render_size, text, font),
            text,
            fill=cls.FONT_COLOR,
            font=font,
        )
        stream = BytesIO()
        image = image.resize((size, size), Image.ANTIALIAS)
        image.save(stream, format=filetype, optimize=True)
        return stream.getvalue()

    @staticmethod
    def _background_color(s):
        """
        Generate a random background color.
        Brighter colors are dropped, because the text is white.
        :param s: Seed used by the random generator
        (same seed will produce the same color).
        """
        seed(s)
        r = v = b = 255
        while r + v + b > 255 * 2:
            r = randint(0, 255)
            v = randint(0, 255)
            b = randint(0, 255)
        return r, v, b

    @staticmethod
    def _font(size):
        """
        Returns a PIL ImageFont instance.
        :param size: size of the avatar, in pixels
        """
        # path = pathlib.Path(".").joinpath("Inconsolata.otf")
        path = os.path.join(os.path.dirname(__file__), "Inconsolata.otf")
        return ImageFont.truetype(path, size=int(0.8 * size))

    @staticmethod
    def _text(string):
        """
        Returns the text to draw.
        """
        return string[0].upper()

    @staticmethod
    def _text_position(size, text, font):
        """
        Returns the left-top point where the text should be positioned.
        """
        width, height = font.getsize(text)
        left = (size - width) / 2.0
        # I just don't know why 5.5, but it seems to be the good ratio
        top = (size - height) / 5.5
        return left, top
