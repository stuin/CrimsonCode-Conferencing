

if __name__ == "__main__":
	try:
		if(len(sys.argv) < 3):
			print('Usage : python player.py hostname')
			sys.exit()

		sys.exit(chat_client(sys.argv[1], 1234))
	except KeyboardInterrupt:
		print('Interrupted')
		sys.exit(0)