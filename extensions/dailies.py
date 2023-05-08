from classes.catboys import CatBoys
from classes.thecatapi import TheCatApi
from classes.zerochan import ZeroChan


def daily_images():
    """Invoke all daily images classes."""
    try:
        CatBoys().invoke_catboys()
    except Exception as e:
        print(f'CB: {e}')

    try:
        ZeroChan().invoke_catgirls()
    except Exception as e:
        print(f'ZC: {e}')

    try:
        TheCatApi().invoke_cats()
    except Exception as e:
        print(f'TCA: {e}')