from bot import notify,setup
from farm_with_numbers import polling

if __name__ == '__main__':
	polling(notify=notify)
	setup()
