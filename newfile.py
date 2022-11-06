import secrets

with open("config", "w") as f:
	f.write(secrets.token_hex())