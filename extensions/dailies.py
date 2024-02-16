from classes.catboys import CatBoys
from classes.thecatapi import TheCatApi
from classes.zerochan import ZeroChan


def daily_images():
    """Invoke all daily images classes."""
    try:
        # CatBoys().invoke_catboys()
        ZeroChan(False).invoke_img()
    except Exception as e:
        # print(f'CB: {e}')
        print(f"ZCB: {e}")

    try:
        ZeroChan().invoke_img()
    except Exception as e:
        print(f'ZCG: {e}')

    try:
        TheCatApi().invoke_cats()
    except Exception as e:
        print(f'TCA: {e}')